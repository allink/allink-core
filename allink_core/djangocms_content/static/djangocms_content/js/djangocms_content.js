$(function(){

    function toggle_parallax_checkbox() {

        if( document.getElementById('id_bg_image').files && document.getElementById('id_bg_image').files.length > 0 ){
            console.log('files selected');
        }else {
            console.log( 'no file selected' );
        }

    }

    // on page load
    // toggle_parallax_checkbox();

    // not working, because Django CMS sets the input's value with JS (which doesn't fire the change event)
    $('#id_bg_image').on( 'change', function( e ) {
        // toggle_parallax_checkbox();
    });



})
