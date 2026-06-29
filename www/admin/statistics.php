<?php

/**
 * Aggregated view over data/stats.log written by api/statistics.php. No database - reads the
 * flat log file and renders plain PHP/HTML tables.
 *
 * Token-gated via a lightly obfuscated hardcoded token. Visit this page as
 * statistics.php?token=<token>.
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

function eyoc_substr($value, $start, $length)
{
    if (function_exists('mb_substr')) {
        return mb_substr($value, $start, $length);
    }
    return substr($value, $start, $length);
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

function eyoc_resolve_readable_log_file()
{
    $candidates = eyoc_candidate_log_files();
    $fallback = isset($candidates[0]) ? $candidates[0] : '';

    foreach ($candidates as $candidate) {
        if (is_file($candidate) && is_readable($candidate)) {
            return $candidate;
        }
    }

    return $fallback;
}

function eyoc_normalize_month($value)
{
    if (!is_string($value)) {
        return 'unknown';
    }

    if (preg_match('/^\d{4}-\d{2}-\d{2}$/', $value)) {
        return eyoc_substr($value, 0, 7);
    }

    return 'unknown';
}

function eyoc_render_key_value_table($title, $rows, $headers, $limit)
{
    $html = '<h2>' . htmlspecialchars($title) . "</h2>\n<table border=\"1\" cellpadding=\"6\" cellspacing=\"0\">\n<tr>";
    foreach ($headers as $header) {
        $html .= '<th>' . htmlspecialchars($header) . '</th>';
    }
    $html .= "</tr>\n";

    $count = 0;
    foreach ($rows as $row) {
        if ($limit > 0 && $count >= $limit) {
            break;
        }
        $count++;
        $html .= '<tr>';
        foreach ($row as $value) {
            $html .= '<td>' . htmlspecialchars((string) $value) . '</td>';
        }
        $html .= "</tr>\n";
    }

    return $html . "</table>\n";
}

$expectedToken = str_rot13('ohov');
$providedToken = isset($_GET['token']) ? (string) $_GET['token'] : '';

if (!eyoc_hash_equals($expectedToken, $providedToken)) {
    eyoc_status(403, 'Forbidden');
    header('Content-Type: text/plain; charset=utf-8');
    echo "Forbidden.\n\nLoad this page as statistics.php?token=<token>.\n";
    exit;
}

$logFile = eyoc_resolve_readable_log_file();
$byDay = array();
$byMonth = array();
$byPath = array();
$byReferrer = array();
$byCountry = array();
$total = 0;
$logFileExists = $logFile !== '' && file_exists($logFile);
$logFileReadable = $logFileExists && is_readable($logFile);

if ($logFileReadable) {
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
            $month = eyoc_normalize_month($day);
            $path = isset($entry['path']) ? (string) $entry['path'] : '';
            $referrer = isset($entry['referrer']) ? (string) $entry['referrer'] : '';
            $country = isset($entry['country']) ? trim((string) $entry['country']) : '';
            if ($country === '') {
                $country = 'Unknown';
            }
            $byDay[$day] = (isset($byDay[$day]) ? $byDay[$day] : 0) + 1;
            $byMonth[$month] = (isset($byMonth[$month]) ? $byMonth[$month] : 0) + 1;
            $byPath[$path] = (isset($byPath[$path]) ? $byPath[$path] : 0) + 1;
            $byCountry[$country] = (isset($byCountry[$country]) ? $byCountry[$country] : 0) + 1;
            if ($referrer !== '') {
                $byReferrer[$referrer] = (isset($byReferrer[$referrer]) ? $byReferrer[$referrer] : 0) + 1;
            }
        }
        flock($fh, LOCK_UN);
        fclose($fh);
    }
}

ksort($byDay);
ksort($byMonth);
arsort($byPath);
arsort($byReferrer);
arsort($byCountry);

$recentDailyRows = array();
$recentDailyLimit = 31;
$recentSlice = array_slice($byDay, -$recentDailyLimit, null, true);
$runningTotal = 0;
foreach ($recentSlice as $day => $count) {
    $runningTotal += (int) $count;
    $recentDailyRows[] = array($day, (int) $count, $runningTotal);
}

$monthlyRows = array();
foreach (array_reverse($byMonth, true) as $month => $count) {
    $monthlyRows[] = array($month, (int) $count);
}

$countryRows = array();
foreach ($byCountry as $country => $count) {
    $countryRows[] = array($country, (int) $count);
}

$pathRows = array();
foreach ($byPath as $path => $count) {
    $pathRows[] = array($path, (int) $count);
}

$referrerRows = array();
foreach ($byReferrer as $referrer => $count) {
    $referrerRows[] = array($referrer, (int) $count);
}

eyoc_disable_cache();
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
<?php if (!$logFileExists) { ?>
<p><strong>Warning:</strong> log file not found at the resolved location.</p>
<?php } elseif (!$logFileReadable) { ?>
<p><strong>Warning:</strong> log file exists but is not readable by PHP.</p>
<?php } ?>
<?php echo eyoc_render_key_value_table('Recent 31 days', $recentDailyRows, array('Day', 'Hits', 'Cumulative'), 0); ?>
<?php echo eyoc_render_key_value_table('Monthly totals', $monthlyRows, array('Month', 'Hits'), 0); ?>
<?php echo eyoc_render_key_value_table('Top countries', $countryRows, array('Country', 'Hits'), 25); ?>
<?php echo eyoc_render_key_value_table('Top pages', $pathRows, array('Page', 'Hits'), 25); ?>
<?php echo eyoc_render_key_value_table('Top referrers', $referrerRows, array('Referrer', 'Hits'), 25); ?>
</body>
</html>
