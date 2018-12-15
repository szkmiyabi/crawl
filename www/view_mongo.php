<?php

$mongo = new Mongo();
$db = $mongo->selectDB("scraping");
$coll = $db->selectCollection("links");

$docs = $coll->find();

foreach($docs as $id => $obj) {
    print "<pre>";
    print var_dump($obj);
    print "<pre><hr>";
}