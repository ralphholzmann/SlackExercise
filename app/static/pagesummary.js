$(document).ready(function() {
    $('#summary-spinner').hide();
    $(document).ajaxStart(function(){
        $('#summary-spinner').show();
    });
    $(document).ajaxStop(function(){
        $('#summary-spinner').hide();
    });

    // Handle highlighting of source
    var SCROLLTOP_OFFSET = 100;
    var removeHighlighting = function() {
        var sourceTag = $('.page-source')[0];
        sourceTag.innerHTML = sourceTag.innerHTML.replace(
            /<span class="highlight">(&lt;\/?\s*[a-zA-Z0-9]+?\s*?.*?&gt;)<\/span>/gim,
            "$1");
    };
    $('body').on('click', '.tag-name', function(event) {
        event.preventDefault();
        removeHighlighting();
        var tagName = $(this)[0].innerHTML;
        var sourceTag = $('.page-source')[0];
        var pattern = new RegExp('&lt;\/{0,1}\\s*' + tagName + '(\\s+?.*?)*?&gt;', 'gim');
        sourceTag.innerHTML = sourceTag.innerHTML.replace(
            pattern,
            '<span class="highlight">$&</span>');
        $('html, body').animate({
            scrollTop: $(".highlight").offset().top - SCROLLTOP_OFFSET
        }, 200);
    });
    
    // Add summary of page
    var buildSummary = function(response) {
        if (!response || !response.summary || !response.source) {
            $('.error').show();
            return;
        }
        $('.error').hide();
        $('.summary').remove();
        $('.source').remove();
        var summaryContainer = $('<div class="container source"></div>');
        var summaryHeader = $('<div class="header"><h2>Tag Summary<h2></div>');
        var headerRow = $('<div class="row">' +
                            '<div class="col-sm-4 text-center">' +
                              '<h4>Tag</h4>' +
                            '</div>' +
                            '<div class="col-sm-4 text-center">' +
                              '<h4>Count</h4>' +
                            '</div>' +
                          '</div>');
        summaryContainer.append(summaryHeader);
        summaryContainer.append(headerRow);
        _.each(_.pairs(response.summary), function(tag) {
            var name = tag[0];
            var count = tag[1];
            var tagSummary = $('<div class="row">' +
                                  '<div class="col-sm-4 text-center">' +
                                         '<a href class="tag-name">' + name + '</a>' +
                                  '</div>' +
                                  '<div class="col-sm-4 text-center">' +
                                         '<span>' + count + '</span>' +
                                  '</div>' +
                                 '</div>');
            summaryContainer.append(tagSummary);
        });
        $('body').append(summaryContainer);
        var sourceContainer = $('<div class="container source"></div>');
        var sourceHeader = $('<div class="header"><h2> Page Source </h2></div>');
        sourceContainer.append(sourceHeader);
        var source = $('<pre class="page-source-container">' +
                          '<code class="page-source">' +
                          '</code>' +
    '                   </pre>');
        sourceContainer.append(source);
        $('body').append(sourceContainer);
        $('.page-source').text(response.source);
    };
    
    // Handle form submission via AJAX
    $('.form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            url: '/pagesummary',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                buildSummary(response);
            },
            error: function(error) {
                console.log(error);
                $('.error').show();
            }
        });
    });

});
