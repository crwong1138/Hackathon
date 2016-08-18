<html xmlns="http://www.w3.org/1999/xhtml">

<!-- yes, i know this space is incorrect but it makes the rest work -->
<DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<head>
    <title>UberGallery</title>
    <link rel="shortcut icon" href="<?php echo THEMEPATH; ?>/images/favicon.png" />

    <link rel="stylesheet" type="text/css" href="<?php echo THEMEPATH; ?>/rebase-min.css" />
    <link rel="stylesheet" type="text/css" href="<?php echo THEMEPATH; ?>/style.css" />
    <?php echo $gallery->getColorboxStyles(5); ?>

    <script type="text/javascript" src="resources/colorbox/jquery-2.1.4.min.js"></script>
    <?php echo $gallery->getColorboxScripts(); ?>

    <?php file_exists('googleAnalytics.inc') ? include('googleAnalytics.inc') : false; ?>

</head>
<body>

<!-- Start UberGallery v<?php echo UberGallery::VERSION; ?> - Copyright (c) <?php echo date('Y'); ?> Chris Kankiewicz (http://www.ChrisKankiewicz.com) -->
<!-- blue theme -->
<div id="galleryWrapper">

<div class="mark">
  <div class="lefty">
    <h1>NetApp Hackathon</h1>
  </div>

  <div class="righty">
      <?php
        $url = "//{$_SERVER['HTTP_HOST']}{$_SERVER['DOCUMENT_URI']}";
        $escaped_url = htmlspecialchars( $url, ENT_QUOTES, 'UTF-8' );
        echo '<a href="' . $escaped_url . '?take" class="snapclick">' . "Take a new picture!" . '</a>';
      ?>
  </div>
  <br/>
</div>


    <div class="line"></div>

    <?php
      if(isset($_GET["take"])) {
        $img = exec("pibooth/takepicture.py");
        if(preg_match("#^images/takepicture_\d{8}-\d{6}.png$#", $img)) {
          $pimg = 'pibooth/' . $img;
          print('<a href="' . $pimg . '" title="' . $pimg . '" rel="colorbox">' . "\r\n");
          print('  <img id="galleryHiLitePic" src="' . $pimg . '" alt="Image ' . $pimg . '"' . ">\r\n</a>\r\n");
          print('<div class="line"></div>' . "\r\n");
        }
        // sync the new image to AWS (in the background)
        exec("pibooth/syncimages.py > /dev/null &");
      } else {
        $img = $_GET["img"];
        if(preg_match("#^images/takepicture_\d{8}-\d{6}.png$#", $img)) {
          $pimg = 'pibooth/' . $img;
          print('<a href="' . $pimg . '" title="' . $pimg . '" rel="colorbox">' . "\r\n");
          print('  <img id="galleryHiLitePic" src="' . $pimg . '" alt="Image ' . $pimg . '"' . ">\r\n</a>\r\n");
          print('<div class="line"></div>' . "\r\n");
        }

      }
    ?>    

    <?php if($gallery->getSystemMessages()): ?>
        <ul id="systemMessages">
            <?php foreach($gallery->getSystemMessages() as $message): ?>
                <li class="<?php echo $message['type']; ?>">
                    <?php echo $message['text']; ?>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>

    <div id="galleryListWrapper">
      <?php if (!empty($galleryArray) && $galleryArray['stats']['total_images'] > 0): ?>
        <ul id="galleryList" class="clearfix">
          <?php foreach ($galleryArray['images'] as $image): ?>
            <li>
              <!-- crackers -->
              <a href="<?php echo html_entity_decode($image['file_path']); ?>" title="<?php echo $image['file_title']; ?>" rel="colorbox" >
                <img src="<?php echo $image['thumb_path']; ?>" alt="<?php echo $image['file_title']; ?>"/>
              </a>
            </li>
          <?php endforeach; ?>
        </ul>
      <?php endif; ?>
    </div>

    <div class="line"></div>
    <div id="galleryFooter" class="clearfix">

        <?php if ($galleryArray['stats']['total_pages'] > 1): ?>
        <ul id="galleryPagination">

            <?php foreach ($galleryArray['paginator'] as $item): ?>

                <li class="<?php echo $item['class']; ?>">
                    <?php if (!empty($item['href'])): ?>
                        <a href="<?php echo $item['href']; ?>"><?php echo $item['text']; ?></a>
                    <?php else: ?><?php echo $item['text']; ?><?php endif; ?>
                </li>

            <?php endforeach; ?>

        </ul>
        <?php endif; ?>

        <div id="credit">Powered by <a href="http://www.ubergallery.net">UberGallery</a></div>
    </div>
</div>
<!-- End UberGallery - Distributed under the MIT license: http://www.opensource.org/licenses/mit-license.php -->

</body>
</html>
