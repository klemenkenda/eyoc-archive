<?php

/**
 * Visitor-stats logging endpoint. No database - appends one JSON line per pageview to
 * data/stats.log under flock() for safe concurrent writes. Logs only path + referrer +
 * a day-bucketed date (server-generated, not the client's clock) - no IP address, no
 * full user-agent string, no cookies/sessions.
 */

function eyoc_status($code, $text)
{
    header('HTTP/1.1 ' . (int) $code . ' ' . $text);
}

function eyoc_disable_cache()
{
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Cache-Control: post-check=0, pre-check=0', false);
    header('Pragma: no-cache');
    header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
}

function eyoc_substr($value, $start, $length)
{
    if (function_exists('mb_substr')) {
        return mb_substr($value, $start, $length);
    }
    return substr($value, $start, $length);
}

function eyoc_normalize_country($value)
{
    if (!is_string($value)) {
        return '';
    }

    $value = trim($value);
    if ($value === '') {
        return '';
    }

    if (preg_match('/^[A-Za-z]{2}$/', $value)) {
        return strtoupper($value);
    }

    return eyoc_substr($value, 0, 60);
}

function eyoc_country_from_language($value)
{
    if (!is_string($value) || $value === '') {
        return '';
    }

    if (preg_match('/^[a-z]{2,3}[-_]([A-Za-z]{2})\b/', $value, $matches)) {
        return strtoupper($matches[1]);
    }

    return '';
}

function eyoc_detect_country()
{
    $serverKeys = array(
        'HTTP_CF_IPCOUNTRY',
        'GEOIP_COUNTRY_CODE',
        'HTTP_X_COUNTRY_CODE',
        'HTTP_X_COUNTRY',
        'HTTP_X_APPENGINE_COUNTRY',
        'HTTP_X_VERCEL_IP_COUNTRY',
        'HTTP_X_COUNTRY_ISO',
    );

    foreach ($serverKeys as $key) {
        if (isset($_SERVER[$key])) {
            $country = eyoc_normalize_country($_SERVER[$key]);
            if ($country !== '') {
                return $country;
            }
        }
    }

    if (isset($_SERVER['HTTP_ACCEPT_LANGUAGE'])) {
        return eyoc_country_from_language($_SERVER['HTTP_ACCEPT_LANGUAGE']);
    }

    return '';
}

function eyoc_candidate_log_files()
{
    $candidates = array(
        __DIR__ . '/../data/stats.log',
    );

    if (isset($_SERVER['DOCUMENT_ROOT']) && is_string($_SERVER['DOCUMENT_ROOT']) && $_SERVER['DOCUMENT_ROOT'] !== '') {
        $candidates[] = rtrim($_SERVER['DOCUMENT_ROOT'], "/\\") . '/data/stats.log';
    }

    if (isset($_SERVER['SCRIPT_FILENAME']) && is_string($_SERVER['SCRIPT_FILENAME']) && $_SERVER['SCRIPT_FILENAME'] !== '') {
        $candidates[] = dirname(dirname($_SERVER['SCRIPT_FILENAME'])) . '/data/stats.log';
    }

    $unique = array();
    $seen = array();
    foreach ($candidates as $candidate) {
        $key = str_replace('\\', '/', $candidate);
        if (!isset($seen[$key])) {
            $seen[$key] = true;
            $unique[] = $candidate;
        }
    }

    return $unique;
}

function eyoc_resolve_writable_log_file()
{
    $candidates = eyoc_candidate_log_files();

    foreach ($candidates as $candidate) {
        $dir = dirname($candidate);
        if (!is_dir($dir) || !is_writable($dir)) {
            continue;
        }
        if (!file_exists($candidate) || is_writable($candidate)) {
            return $candidate;
        }
    }

    return isset($candidates[0]) ? $candidates[0] : '';
}

$requestMethod = isset($_SERVER['REQUEST_METHOD']) ? $_SERVER['REQUEST_METHOD'] : '';
eyoc_disable_cache();
if ($requestMethod !== 'POST') {
    eyoc_status(405, 'Method Not Allowed');
    header('Content-Type: application/json');
    echo json_encode(array('error' => 'POST only'));
    exit;
}

$rawBody = file_get_contents('php://input');
$body = json_decode($rawBody !== false ? $rawBody : '', true);

$path = is_array($body) && isset($body['path']) ? (string) $body['path'] : '';
$referrer = is_array($body) && isset($body['referrer']) ? (string) $body['referrer'] : '';

// Bound the log line size regardless of what the client sends.
$path = eyoc_substr($path, 0, 200);
$referrer = eyoc_substr($referrer, 0, 200);

$entry = array(
    'date' => gmdate('Y-m-d'),
    'path' => $path,
    'referrer' => $referrer,
    'country' => eyoc_detect_country(),
);

$logFile = eyoc_resolve_writable_log_file();
$fh = fopen($logFile, 'a');
if ($fh !== false) {
    flock($fh, LOCK_EX);
    fwrite($fh, json_encode($entry) . "\n");
    flock($fh, LOCK_UN);
    fclose($fh);
} else {
    error_log('EYOC stats: unable to open log file for writing: ' . $logFile);
}

eyoc_status(204, 'No Content');
