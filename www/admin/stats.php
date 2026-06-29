<?php

/**
 * Aggregated view over data/stats.log written by api/stats.php. No database - reads the
 * flat log file and renders plain PHP/HTML tables.
 *
 * Token-gated via a lightly obfuscated hardcoded token. Visit this page as
 * stats.php?token=<token>.
 */

function eyoc_status($code, $text)
{
    header('HTTP/1.1 ' . (int) $code . ' ' . $text);
}

function eyoc_hash_equals($known, $user)
{
    if (function_exists('hash_equals')) {
        return hash_equals($known, $user);
    }

    if (!is_string($known) || !is_string($user)) {
        return false;
    }

    $knownLen = strlen($known);
    if ($knownLen !== strlen($user)) {
        return false;
    }

    $result = 0;
    for ($i = 0; $i < $knownLen; $i++) {
        $result |= ord($known[$i]) ^ ord($user[$i]);
    }
    return $result === 0;
}

$expectedToken = str_rot13('ohov');
$providedToken = isset($_GET['token']) ? (string) $_GET['token'] : '';

if (!eyoc_hash_equals($expectedToken, $providedToken)) {
    eyoc_status(403, 'Forbidden');
    header('Content-Type: text/plain; charset=utf-8');
    echo "Forbidden.\n\nLoad this page as stats.php?token=<token>.\n";
    exit;
}

$logFile = __DIR__ . '/../data/stats.log';
$byDay = array();
$byPath = array();
$byReferrer = array();
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
            $day = isset($entry['date']) ? (string) $entry['date'] : 'unknown';
            $path = isset($entry['path']) ? (string) $entry['path'] : '';
            $referrer = isset($entry['referrer']) ? (string) $entry['referrer'] : '';
            $byDay[$day] = (isset($byDay[$day]) ? $byDay[$day] : 0) + 1;
            $byPath[$path] = (isset($byPath[$path]) ? $byPath[$path] : 0) + 1;
            if ($referrer !== '') {
                $byReferrer[$referrer] = (isset($byReferrer[$referrer]) ? $byReferrer[$referrer] : 0) + 1;
            }
        }
        flock($fh, LOCK_UN);
        fclose($fh);
    }
}

ksort($byDay);
arsort($byPath);
arsort($byReferrer);

function eyoc_render_table($title, $rows, $limit)
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
<p>Total logged pageviews: <strong><?php echo (int) $total; ?></strong></p>
<?php echo eyoc_render_table('Hits per day', $byDay, 25); ?>
<?php echo eyoc_render_table('Top pages', $byPath, 25); ?>
<?php echo eyoc_render_table('Top referrers', $byReferrer, 25); ?>
</body>
</html>
