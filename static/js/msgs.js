function run(state,msg){

  console.log(msg);
  $(window).on('load',function() {
  $('<div style="position:absolute; width:100%; opacity: 0.95;" class="alert text-white d-flex justify-content-center alert-'+state+'">' + msg + '</div>')
//   $('<div style="position:absolute; width:100%; opacity: 0.95;" class = "text-white d-flex justify-content-center">' + msg + '</div>')
  .appendTo('#header')
  .hide()
  .slideDown()
  .delay(5000)
  .slideUp(function() {
   $(this).remove();
  });
  return false;
});
}


// (function($) {
//   var $app = $('.navbar');
 
//   var notifications = {
//    init: function() {
//     $app.on('notify', function(e) {
 
//      $('<div class="alert alert-success">' + e.message + '</div>')
//       .appendTo('.msghere')
//       .hide()
//       .slideDown()
//       .delay(2000)
//       .slideUp(function() {
//        $(this).remove();
//       });
//     });
//    }
//   };
 
//   var sampleModule = {
//    init: function() {
      
//     $(window).on('load',function() {
//      var msgs = $('#messages li');

//   msgs.each(function(idx, li) {
//       var msg = $(li);
//       $app.trigger({
//           type: 'notify',
//           message: msg.text()
//              });
  
//   });
     
//      return false;
//     });
//    }
//   };
 
//   notifications.init();
//   sampleModule.init();
//  })(jQuery);