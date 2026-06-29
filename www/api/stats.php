<?php
declare(strict_types=1);

/**
 * Visitor-stats logging endpoint. No database - appends one JSON line per pageview to
 * data/stats.log under flock() for safe concurrent writes. Logs only path + referrer +
 * a day-bucketed date (server-generated, not the client's clock) - no IP address, no
 * full user-agent string, no cookies/sessions.
 */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'POST only']);
    exit;
}

$body = json_decode((string) file_get_contents('php://input'), true);

$path = is_array($body) && isset($body['path']) ? (string) $body['path'] : '';
$referrer = is_array($body) && isset($body['referrer']) ? (string) $body['referrer'] : '';

// Bound the log line size regardless of what the client sends.
$path = mb_substr($path, 0, 200);
$referrer = mb_substr($referrer, 0, 200);

$entry = [
    'date' => gmdate('Y-m-d'),
    'path' => $path,
    'referrer' => $referrer,
];

$logFile = __DIR__ . '/../data/stats.log';
$fh = fopen($logFile, 'a');
if ($fh !== false) {
    flock($fh, LOCK_EX);
    fwrite($fh, json_encode($entry, JSON_UNESCAPED_SLASHES) . "\n");
    flock($fh, LOCK_UN);
    fclose($fh);
}

http_response_code(204);
