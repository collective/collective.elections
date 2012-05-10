$(document).ready(function() {

    $('a.cast-vote').prepOverlay({
         subtype: 'ajax',
         filter: '#content>*',
         formselector: 'form',
         noform: 'reload'
        });

});