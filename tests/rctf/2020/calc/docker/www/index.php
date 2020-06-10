<?php
error_reporting(0);
if(!isset($_GET['num'])){
    show_source(__FILE__);
}else{
    $str = $_GET['num'];
    $blacklist = ['[a-z]', '[\x7f-\xff]', '\s',"'", '"', '`', '\[', '\]','\$', '_', '\\\\','\^', ','];
    foreach ($blacklist as $blackitem) {
        if (preg_match('/' . $blackitem . '/im', $str)) {
            die("what are you want to do?\n<BR>");
            break;
        }
    }
    @eval('echo '.$str.';');
}
?>