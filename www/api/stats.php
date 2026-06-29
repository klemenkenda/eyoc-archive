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

function eyoc_substr($value, $start, $length)
{
    if (function_exists('mb_substr')) {
        return mb_substr($value, $start, $length);
    }
    return substr($value, $start, $length);
}

$requestMethod = isset($_SERVER['REQUEST_METHOD']) ? $_SERVER['REQUEST_METHOD'] : '';
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
);

$logFile = __DIR__ . '/../data/stats.log';
$fh = fopen($logFile, 'a');
if ($fh !== false) {
    flock($fh, LOCK_EX);
    fwrite($fh, json_encode($entry) . "\n");
    flock($fh, LOCK_UN);
    fclose($fh);
}

eyoc_status(204, 'No Content');
