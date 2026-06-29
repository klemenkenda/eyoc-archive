<?php
declare(strict_types=1);

/**
 * Aggregated view over data/stats.log written by api/stats.php. No database - reads the
 * flat log file and renders plain PHP/HTML tables.
 *
 * Token-gated: set the EYOC_ADMIN_TOKEN environment variable on the server (host control
 * panel / php-fpm pool config), then visit this page as stats.php?token=<that value>.
 * Without the env var set, this page always refuses access.
 */

$expectedToken = getenv('EYOC_ADMIN_TOKEN');
$providedToken = $_GET['token'] ?? '';

if ($expectedToken === false || $expectedToken === '' || !hash_equals($expectedToken, (string) $providedToken)) {
    http_response_code(403);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Forbidden.\n\nSet the EYOC_ADMIN_TOKEN environment variable on the server, then load this\npage as stats.php?token=<that value>.\n";
    exit;
}

$logFile = __DIR__ . '/../data/stats.log';
$byDay = [];
$byPath = [];
$byReferrer = [];
$total = 0;

if (file_exists($logFile)) {
    $fh = fopen($logFile, 'r');
    if ($fh !== false) {
        flock($fh, LOCK_SH);
        while (($line = fgets($fh)) !== false) {
            $entry = json_decode($line, true);
            if (!is_array($entry)) {
                continue;
            }
            $total++;
            $day = (string) ($entry['date'] ?? 'unknown');
            $path = (string) ($entry['path'] ?? '');
            $referrer = (string) ($entry['referrer'] ?? '');
            $byDay[$day] = ($byDay[$day] ?? 0) + 1;
            $byPath[$path] = ($byPath[$path] ?? 0) + 1;
            if ($referrer !== '') {
                $byReferrer[$referrer] = ($byReferrer[$referrer] ?? 0) + 1;
            }
        }
        flock($fh, LOCK_UN);
        fclose($fh);
    }
}

ksort($byDay);
arsort($byPath);
arsort($byReferrer);

function eyoc_render_table(string $title, array $rows, int $limit = 25): string
{
    $html = '<h2>' . htmlspecialchars($title) . "</h2>\n<table border=\"1\" cellpadding=\"6\" cellspacing=\"0\">\n";
    $html .= "<tr><th>Key</th><th>Count</th></tr>\n";
    $i = 0;
    foreach ($rows as $key => $count) {
        if ($i++ >= $limit) {
            break;
        }
        $html .= '<tr><td>' . htmlspecialchars((string) $key) . '</td><td>' . (int) $count . "</td></tr>\n";
    }
    return $html . "</table>\n";
}

header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>EYOC Archive — visitor stats</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; }
  table { border-collapse: collapse; margin-bottom: 2rem; width: 100%; }
  th, td { padding: 0.4rem 0.6rem; text-align: left; }
  th { background: #eef1f5; }
</style>
</head>
<body>
<h1>EYOC Archive — visitor stats</h1>
<p>Total logged pageviews: <strong><?= (int) $total ?></strong></p>
<?= eyoc_render_table('Hits per day', $byDay) ?>
<?= eyoc_render_table('Top pages', $byPath) ?>
<?= eyoc_render_table('Top referrers', $byReferrer) ?>
</body>
</html>
