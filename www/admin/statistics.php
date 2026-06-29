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

function eyoc_max_metric($rows, $index)
{
    $max = 0;
    foreach ($rows as $row) {
        $value = isset($row[$index]) ? (int) $row[$index] : 0;
        if ($value > $max) {
            $max = $value;
        }
    }
    return $max;
}

function eyoc_render_bar_chart($title, $rows, $labelIndex, $valueIndex, $limit)
{
    $slice = $limit > 0 ? array_slice($rows, 0, $limit) : $rows;
    $max = eyoc_max_metric($slice, $valueIndex);
    $html = '<section class="stats-panel"><h2>' . htmlspecialchars($title) . "</h2>\n";

    if (count($slice) === 0) {
        return $html . "<p class=\"stats-empty\">No data yet.</p></section>\n";
    }

    $html .= "<div class=\"bar-list\">\n";
    foreach ($slice as $row) {
        $label = isset($row[$labelIndex]) ? (string) $row[$labelIndex] : '';
        $value = isset($row[$valueIndex]) ? (int) $row[$valueIndex] : 0;
        $width = $max > 0 ? max(2, (int) floor(($value / $max) * 100)) : 0;
        $html .= "<div class=\"bar-row\">\n";
        $html .= '<div class="bar-meta"><span class="bar-label">' . htmlspecialchars($label) . '</span><span class="bar-value">' . $value . "</span></div>\n";
        $html .= '<div class="bar-track"><div class="bar-fill" style="width:' . $width . '%"></div></div>' . "\n";
        $html .= "</div>\n";
    }
    $html .= "</div></section>\n";

    return $html;
}

function eyoc_render_daily_chart($title, $rows)
{
    $width = 720;
    $height = 240;
    $left = 44;
    $right = 12;
    $top = 12;
    $bottom = 30;
    $plotWidth = $width - $left - $right;
    $plotHeight = $height - $top - $bottom;
    $count = count($rows);
    $hitMax = eyoc_max_metric($rows, 1);
    $cumMax = eyoc_max_metric($rows, 2);

    $bars = array();
    $line = array();
    $labels = array();
    $html = '<section class="stats-panel stats-panel-wide"><h2>' . htmlspecialchars($title) . "</h2>\n";

    if ($count === 0) {
        return $html . "<p class=\"stats-empty\">No data yet.</p></section>\n";
    }

    $barWidth = max(6, (int) floor($plotWidth / max($count, 1)) - 4);
    for ($i = 0; $i < $count; $i++) {
        $row = $rows[$i];
        $day = isset($row[0]) ? (string) $row[0] : '';
        $hits = isset($row[1]) ? (int) $row[1] : 0;
        $cum = isset($row[2]) ? (int) $row[2] : 0;
        $x = $left + (int) floor(($i + 0.5) * ($plotWidth / max($count, 1)));
        $barHeight = $hitMax > 0 ? (int) floor(($hits / $hitMax) * ($plotHeight - 10)) : 0;
        $barY = $top + $plotHeight - $barHeight;
        $cumY = $cumMax > 0 ? $top + $plotHeight - (int) floor(($cum / $cumMax) * ($plotHeight - 6)) : $top + $plotHeight;
        $bars[] = '<rect x="' . ($x - (int) floor($barWidth / 2)) . '" y="' . $barY . '" width="' . $barWidth . '" height="' . max(1, $barHeight) . '" rx="3"></rect>';
        $line[] = $x . ',' . $cumY;
        if ($i === 0 || $i === $count - 1 || $i === (int) floor(($count - 1) / 2)) {
            $labels[] = '<text x="' . $x . '" y="' . ($height - 8) . '" text-anchor="middle">' . htmlspecialchars(eyoc_substr($day, 5, 5)) . '</text>';
        }
    }

    $html .= "<div class=\"chart-legend\"><span><i class=\"legend-bar\"></i>Hits</span><span><i class=\"legend-line\"></i>Cumulative</span></div>\n";
    $html .= '<svg class="stats-chart" viewBox="0 0 ' . $width . ' ' . $height . '" role="img" aria-label="' . htmlspecialchars($title) . '">';
    $html .= '<line x1="' . $left . '" y1="' . ($top + $plotHeight) . '" x2="' . ($width - $right) . '" y2="' . ($top + $plotHeight) . '" class="chart-axis"></line>';
    $html .= '<polyline points="' . implode(' ', $line) . '" class="chart-line"></polyline>';
    $html .= '<g class="chart-bars">' . implode('', $bars) . '</g>';
    $html .= '<g class="chart-labels">' . implode('', $labels) . '</g>';
    $html .= '</svg>';
    $html .= "</section>\n";

    return $html;
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
  :root { color-scheme: light; }
  body { font-family: system-ui, sans-serif; margin: 0; background: #f6f8fb; color: #1c2530; }
  .stats-wrap { max-width: 1180px; margin: 0 auto; padding: 1.5rem; }
  h1 { margin: 0 0 0.5rem; color: #1f4e8c; }
  h2 { margin: 0 0 1rem; font-size: 1.1rem; color: #1f4e8c; }
  p { margin: 0.25rem 0 0; }
  .stats-summary { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin: 1.5rem 0; }
  .summary-card, .stats-panel { background: white; border: 1px solid #dde1e6; border-radius: 8px; padding: 1rem 1.1rem; box-shadow: 0 10px 24px rgba(31, 78, 140, 0.06); }
  .summary-card small { display: block; color: #667287; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.04em; }
  .summary-card strong { display: block; margin-top: 0.4rem; font-size: 1.8rem; color: #fe6902; }
  .stats-grid { display: grid; grid-template-columns: minmax(0, 2fr) minmax(320px, 1fr); gap: 1rem; align-items: start; }
  .stats-grid + .stats-grid { margin-top: 1rem; }
  .stats-panel-wide { margin-bottom: 1rem; }
  .stats-empty { color: #667287; }
  .chart-legend { display: flex; gap: 1rem; font-size: 0.9rem; color: #526173; margin-bottom: 0.5rem; }
  .chart-legend span { display: inline-flex; align-items: center; gap: 0.4rem; }
  .legend-bar, .legend-line { display: inline-block; width: 18px; height: 3px; border-radius: 999px; }
  .legend-bar { height: 10px; background: #6b96d9; }
  .legend-line { background: #fe6902; }
  .stats-chart { width: 100%; height: auto; display: block; }
  .chart-axis { stroke: #cfd7e3; stroke-width: 1; }
  .chart-line { fill: none; stroke: #fe6902; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
  .chart-bars rect { fill: #6b96d9; }
  .chart-labels text { fill: #667287; font-size: 12px; }
  .bar-list { display: grid; gap: 0.7rem; }
  .bar-meta { display: flex; justify-content: space-between; gap: 1rem; font-size: 0.92rem; margin-bottom: 0.25rem; }
  .bar-label { color: #1c2530; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .bar-value { color: #526173; font-variant-numeric: tabular-nums; }
  .bar-track { height: 10px; background: #eef2f7; border-radius: 999px; overflow: hidden; }
  .bar-fill { height: 100%; background: linear-gradient(90deg, #2b6dc4, #fe6902); border-radius: 999px; }
  table { border-collapse: collapse; margin: 0; width: 100%; background: white; }
  th, td { padding: 0.55rem 0.65rem; text-align: left; border-bottom: 1px solid #eef2f7; }
  th { background: #eef3f9; color: #405268; }
  .stats-table-panel { margin-top: 1rem; }
  .stats-meta { color: #667287; }
  .stats-warning { color: #b3261e; font-weight: 600; margin-top: 1rem; }
  @media (max-width: 860px) {
    .stats-summary, .stats-grid { grid-template-columns: 1fr; }
    .stats-wrap { padding: 1rem; }
  }
</style>
</head>
<body>
<div class="stats-wrap">
<h1>EYOC Archive — visitor statistics</h1>
<p class="stats-meta">Server-rendered overview from <code>data/stats.log</code>.</p>
<?php if (!$logFileExists) { ?>
<p class="stats-warning">Warning: log file not found at the resolved location.</p>
<?php } elseif (!$logFileReadable) { ?>
<p class="stats-warning">Warning: log file exists but is not readable by PHP.</p>
<?php } ?>
<div class="stats-summary">
  <div class="summary-card"><small>Total pageviews</small><strong><?php echo (int) $total; ?></strong></div>
  <div class="summary-card"><small>Tracked months</small><strong><?php echo count($monthlyRows); ?></strong></div>
  <div class="summary-card"><small>Countries seen</small><strong><?php echo count($countryRows); ?></strong></div>
</div>
<?php echo eyoc_render_daily_chart('Recent 31 days', $recentDailyRows); ?>
<div class="stats-grid">
  <?php echo eyoc_render_bar_chart('Monthly totals', $monthlyRows, 0, 1, 12); ?>
  <?php echo eyoc_render_bar_chart('Top countries', $countryRows, 0, 1, 10); ?>
</div>
<div class="stats-grid">
  <div class="stats-table-panel stats-panel"><?php echo eyoc_render_key_value_table('Recent 31 days', $recentDailyRows, array('Day', 'Hits', 'Cumulative'), 0); ?></div>
  <div class="stats-table-panel stats-panel"><?php echo eyoc_render_key_value_table('Top referrers', $referrerRows, array('Referrer', 'Hits'), 15); ?></div>
</div>
<div class="stats-grid">
  <div class="stats-table-panel stats-panel"><?php echo eyoc_render_key_value_table('Top pages', $pathRows, array('Page', 'Hits'), 25); ?></div>
  <div class="stats-table-panel stats-panel"><?php echo eyoc_render_key_value_table('Country totals', $countryRows, array('Country', 'Hits'), 25); ?></div>
</div>
</div>
</body>
</html>
