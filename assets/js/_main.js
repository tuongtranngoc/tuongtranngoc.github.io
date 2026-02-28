/* ==========================================================================
   jQuery plugin settings and other scripts
   ========================================================================== */

$(document).ready(function(){
   // Sticky footer
  var bumpIt = function() {
      $("body").css("margin-bottom", $(".page__footer").outerHeight(true));
    },
    didResize = false;

  bumpIt();

  $(window).resize(function() {
    didResize = true;
  });
  setInterval(function() {
    if (didResize) {
      didResize = false;
      bumpIt();
    }
  }, 250);
  // FitVids init
  $("#main").fitVids();

  // init sticky sidebar
  $(".sticky").Stickyfill();

  var stickySideBar = function(){
    var show = $(".author__urls-wrapper button").length === 0 ? $(window).width() > 1024 : !$(".author__urls-wrapper button").is(":visible");
    // console.log("has button: " + $(".author__urls-wrapper button").length === 0);
    // console.log("Window Width: " + windowWidth);
    // console.log("show: " + show);
    //old code was if($(window).width() > 1024)
    if (show) {
      // fix
      Stickyfill.rebuild();
      Stickyfill.init();
      $(".author__urls").show();
    } else {
      // unfix
      Stickyfill.stop();
      $(".author__urls").hide();
    }
  };

  stickySideBar();

  $(window).resize(function(){
    stickySideBar();
  });

  // Follow menu drop down

  $(".author__urls-wrapper button").on("click", function() {
    $(".author__urls").fadeToggle("fast", function() {});
    $(".author__urls-wrapper button").toggleClass("open");
  });

  // init smooth scroll
  $("a").smoothScroll({offset: -20});

  // add lightbox class to all image links
  $("a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.png'],a[href$='.gif']").addClass("image-popup");

  // Magnific-Popup options
  $(".image-popup").magnificPopup({
    // disableOn: function() {
    //   if( $(window).width() < 500 ) {
    //     return false;
    //   }
    //   return true;
    // },
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      tError: '<a href="%url%">Image #%curr%</a> could not be loaded.',
    },
    removalDelay: 500, // Delay in milliseconds before popup is removed
    // Class that is added to body when popup is open.
    // make it unique to apply your CSS animations just to this exact popup
    mainClass: 'mfp-zoom-in',
    callbacks: {
      beforeOpen: function() {
        // just a hack that adds mfp-anim class to markup
        this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure mfp-with-anim');
      }
    },
    closeOnContentClick: true,
    midClick: true // allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source.
  });

});

// Search overlay
(function() {
  var overlay  = document.getElementById('search-overlay');
  var input    = document.getElementById('search-input');
  var results  = document.getElementById('search-results');
  var openBtn  = document.getElementById('search-toggle');
  var backdrop = document.getElementById('search-backdrop');

  var idx, docs;

  function openSearch() {
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    input.focus();
    if (!idx) loadIndex();
  }

  function closeSearch() {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    input.value = '';
    results.innerHTML = '';
  }

  function loadIndex() {
    fetch('/search.json')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        docs = data;
        idx = lunr(function() {
          this.ref('url');
          this.field('title', { boost: 10 });
          this.field('tags',  { boost: 5 });
          this.field('content');
          data.forEach(function(d) { this.add(d); }, this);
        });
      });
  }

  function renderResults(query) {
    results.innerHTML = '';
    if (!idx || !query.trim()) return;
    var hits;
    try {
      hits = idx.search(query + '*');
    } catch(e) {
      hits = idx.search(query);
    }
    hits.slice(0, 8).forEach(function(hit) {
      var doc = docs.find(function(d) { return d.url === hit.ref; });
      if (!doc) return;
      var li = document.createElement('li');
      li.className = 'search-result';
      li.innerHTML = '<a href="' + doc.url + '"><span class="search-result__title">'
        + doc.title + '</span></a>';
      results.appendChild(li);
    });
    if (!hits.length) {
      results.innerHTML = '<li class="search-result search-result--empty">No results found.</li>';
    }
  }

  if (openBtn)  openBtn.addEventListener('click', openSearch);
  if (backdrop) backdrop.addEventListener('click', closeSearch);
  if (input)    input.addEventListener('input', function() { renderResults(this.value); });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeSearch();
    if (e.key === 'k' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); openSearch(); }
  });
})();
