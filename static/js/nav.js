
//Template script here

(function($) {
  'use strict' ;
		
	$('nav').coreNavigation({
		menuPosition: "right",
		container: true,	
    	mode: 'sticky',		
				
		onStartSticky: function(){
        	console.log('Start Sticky');
		},
		onEndSticky: function(){
			console.log('End Sticky');
		},
		
		dropdownEvent: 'hover',
		onOpenDropdown: function(){
			console.log('open');
		},
		onCloseDropdown: function(){
			console.log('close');
		},
		
		onInit: function(){
			$('input').keypress(function (e) {
				console.log(e.target.value);
			});
		},
		
		onOpenMegaMenu: function(){
			console.log('Open Megamenu');
		},
		onCloseMegaMenu: function(){
			console.log('Close Megamenu');
		}		
	});	
	
})(jQuery);// End of use strict


// Dynamic active menu
    var path = window.location.pathname.split("/").pop();
    var target = $('header .menu a[href="'+path+'"]');
    target.parent().addClass('active');
    $('header .menu li.active').parents('li').addClass('active');
