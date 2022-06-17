<?php
$path = $argv[1];
$config = json_decode( file_get_contents( '/srv/wstk/var/config.json' ), true );


function varexport($expression, $return=FALSE) {
    $export = var_export($expression, TRUE);
    $export = preg_replace("/^([ ]*)(.*)/m", '$1$1$2', $export);
    $array = preg_split("/\r\n|\n|\r/", $export);
    $array = preg_replace(["/\s*array\s\($/", "/\)(,)?$/", "/\s=>\s$/"], [NULL, ']$1', ' => ['], $array);
    $export = join(PHP_EOL, array_filter(["["] + $array));
    if ((bool)$return) return $export; else echo $export;
}

//$strip_num = preg_replace("/[0-9]+ \=\>/i", '', varexport($config, true));

file_put_contents($path . '/app/etc/env.php', "<?php \nreturn " . varexport($config, true) . ";");
