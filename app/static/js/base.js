var url = document.location.href;

$(document).ready(() => {
  if (window.location.href.indexOf('#bookmarks') != -1) {
    openTabWithURL('bookmarks')
  }
  if (window.location.href.indexOf('#comments') != -1) {
    openTabWithURL('comments')
  }
  new Clipboard('.clipboard-btn', {
    text: function () {
      return url
    }
  });
  // Show / Hide menu when clicked
  $('.has-sub').on('click', function (e) {
    $('.dropdown-menu').not($(this).children('.dropdown-menu')).removeClass('dropdown-shown'); // Hide other menus
    $('.has-sub').not($(this)).removeClass('active');
    $(this).children('.dropdown-menu').toggleClass('dropdown-shown');
    $(this).toggleClass('active');
  });

  // TOGGLE HEADER-NAV
  $('#header-btn').on('click', function (e) {
    $('#header-menu').toggleClass('active');
    $('.nav-btn').toggleClass('active');
    $('body').toggleClass('overflow-hidden');
  });
  $('.dropdown-menu li').on('click', function (e) {
    $('#header-menu').removeClass('active');
    $('.nav-btn').removeClass('active');
    $('body').removeClass('overflow-hidden');
  })
});

$(document).scroll(function () {
  checkOffset();
});

function checkOffset() {
  if ($(window).width() >= 770) {
    if ($('#social-float').offset().top + $('#social-float').height() >=
      $('#footer').offset().top - 10)
      $('#social-float').css('position', 'absolute');
    // Calculate top of social float to not go over footer
    var footerOffset = $('#footer').offset().top;
    var topSocialFloat = $('#social-float').offset().top;
    var bottomSocialFloat = topSocialFloat + $('#social-float').height();
    var diff = footerOffset - bottomSocialFloat;
    var stringTop = '';
    if (diff < 0) {
      topSocialFloat += diff;
      stringTop = topSocialFloat + 'px';
    } else {
      stringTop = topSocialFloat + 'px';
    }
    $('#social-float').css('top', stringTop);
    if ($(document).scrollTop() + window.innerHeight < $('#footer').offset().top && $(document).scrollTop() >= 84) {
      $('#social-float').css('position', 'fixed'); // restore when you scroll up
      $('#social-float').css('top', '25px');
    }
    if ($(document).scrollTop() < 84) {
      $('#social-float').css('position', 'absolute');
      $('#social-float').css('top', '145px');
    }
  } else {
    $('#social-float').css('position', 'relative');
  }
}

function openTab(evt, level) {
  var i, tabcontent, tablevel;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablevel" and remove the class "selected"
  tablevel = document.getElementsByClassName("tablevel");
  for (i = 0; i < tablevel.length; i++) {
    tablevel[i].classList.remove("selected");
  }

  // Show the current tab, and add an "selected" class to the button that opened the tab
  document.getElementById(level).style.display = "block";
  evt.currentTarget.classList.add("selected");
}

function openTabWithURL(level) {
  var i, tabcontent, tablevel;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablevel" and remove the class "selected"
  tablevel = document.getElementsByClassName("tablevel");
  for (i = 0; i < tablevel.length; i++) {
    tablevel[i].classList.remove("selected");
  }

  // Show the current tab, and add an "selected" class to the button that opened the tab
  document.getElementById(level).style.display = "block";
  document.getElementById("tab-".concat(level)).currentTarget.classList.add("selected");
}

var timeout = {};

function displayLinkCopied(id = "0") {
  if (timeout[id]) clearTimeout(timeout[id])
  const popup = $(`#copy-popup-${id}`);
  popup.addClass("show");
  popup.show();
  timeout[id] = setTimeout(() => {
    popup.fadeOut('fast');
    setTimeout(() => {
      popup.removeClass("show");
    }, 500)
  }, 2000);
}

function shareOnFB(url) {
  var link = "https://www.facebook.com/sharer/sharer.php?u=" + url;
  window.open(link);
}

function shareOnTwitter(url) {
  var link = "https://twitter.com/intent/tweet?url=" + url + "&text=" + document.querySelector('#challenge-name').textContent;
  TwitterWindow = window.open(link);
}

function shareOnLinkedIn(url) {
  var link = "https://www.linkedin.com/sharing/share-offsite/?url=" + url;
  window.open(link);
}

function shareOnReddit(url) {
  var link = "https://reddit.com/submit?url=" + url + "&title=" + document.querySelector('#challenge-name').textContent;
  window.open(link);
}


// UNSPLASH Code

//setup before functions
var typingTimer; //timer identifier
var doneTypingInterval = 1000; //time in ms, 5 second for example
var $input = $('#searchWord');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(searchUnsplash, doneTypingInterval);
});

//on keydown, clear the countdown 
$input.on('keydown', function () {
  clearTimeout(typingTimer);
});

function searchUnsplash() {
  var url = new URL("https://api.unsplash.com/search/photos");
  urlArray = [];
  var searchWord = document.getElementById('searchWord').value;

  UNSPLASH_KEY = "";
  params = {
    query: searchWord,
    client_id: UNSPLASH_KEY,
    page: 1

  }
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
  fetch(url).then(res => res.json()).then(data => {
    data.results.forEach(function (item) {
      urlArray.push(item.urls.regular)
    })
  }).then(data => {
    var container = document.getElementById('imageContainer');
    container.innerHTML = "";

    //For each image, create a list that will be contained inside the container
    for (var i = 0, j = urlArray.length; i < j; i++) {
      var list_element = document.createElement('li');
      list_element.setAttribute("id", `image-${i}`); //Create a unique id
      var img = document.createElement('img');
      img.src = urlArray[i]; // img[i] refers to the current URL.
      list_element.appendChild(img);
      list_element.addEventListener("click", function (event) { //Detect when an image is being clicked, and make AJAX request
        container.innerHTML = '<div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>'
        $.ajax({
          type: "POST",
          url: `/addUnsplashPicture/`,
          data: {
            'url': event.target.src,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken').val(),
          },
          success: function () {
            location.reload()
          }
        })
      })
      container.appendChild(list_element);
    }
  })
}

$("#challenge-level").change(function () {
  /* Be careful with SQL injections */
  var selectedLevel = $('#challenge-level').find(":selected").val();

});

$("#login-prompt").hide();

function promptLogin() {
  $("#login-prompt").fadeIn("fast");
}

function dissolveLogin() {
  $("#login-prompt").fadeOut("fast");
}

//Slideshow on the Explore Page
var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) { slideIndex = 1 }
  if (n < 1) { slideIndex = slides.length }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active-dot", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active-dot";
}