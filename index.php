<?php 

  include('resources/UberGallery.php');

  // Initialize the UberGallery object
  $gallery = new UberGallery();

  // Initialize the gallery array
  $galleryArray = $gallery->readImageDirectory('images');


  // Define theme path
  if (!defined('THEMEPATH')) {
    define('THEMEPATH', $gallery->getThemePath());
  }

  // Set path to theme index
  $themeIndex = $gallery->getThemePath(true) . '/index.php';

  // Initialize the theme
  if (file_exists($themeIndex)) {
    include($themeIndex);
  } else {
    die('ERROR: Failed to initialize theme');
  }

?>
