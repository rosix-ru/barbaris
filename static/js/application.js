/* application.js v0.0.1 
 * http://barbaris.foma.su/
###############################################################################
# Copyright 2012 Grigoriy Kramarenko.
###############################################################################
# This file is part of Barbaris.
#
#    Barbaris is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Barbaris is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Barbaris.  If not, see <http://www.gnu.org/licenses/>.
#
# Этот файл — часть Barbaris.
#
#   Barbaris - свободная программа: вы можете перераспространять ее и/или
#   изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
#   в каком она была опубликована Фондом свободного программного обеспечения;
#   либо версии 3 лицензии, либо (по вашему выбору) любой более поздней
#   версии.
#
#   Barbaris распространяется в надежде, что она будет полезной,
#   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
#   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
#   общественной лицензии GNU.
#
#   Вы должны были получить копию Стандартной общественной лицензии GNU
#   вместе с этой программой. Если это не так, см.
#   <http://www.gnu.org/licenses/>.
###############################################################################
*/


$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

!function ($) {
    $(function(){
        
        // Disable certain links in docs
        $('section [href^=#]').click(function (e) {
            e.preventDefault()
        })
        
        // make code pretty
        window.prettyPrint && prettyPrint()
        
        // add-ons
        $('.add-on :checkbox').on('click', function () {
            var $this = $(this),
                method = $this.attr('checked') ? 'addClass' : 'removeClass'
            $(this).parents('.add-on')[method]('active')
        })
        
        // position static twipsies for components page
        if ($(".twipsies a").length) {
            $(window).on('load resize', function () {
                $(".twipsies a").each(function () {
                    $(this)
                        .tooltip({
                            placement: $(this).attr('title'),
                            trigger: 'manual'
                        })
                        .tooltip('show')
                })
            })
        }
        
        // add tipsies to grid for scaffolding
        if ($('#grid-system').length) {
            $('#grid-system').tooltip({
                selector: '.show-grid > div',
                title: function () { return $(this).width() + 'px' }
            })
        }
        
        // fix sub nav on scroll
        var $win = $(window),
            $nav = $('.subnav'),
            navTop = $('.subnav').length && $('.subnav').offset().top - 40,
            isFixed = 0
        
        processScroll()
        
        // hack sad times - holdover until rewrite for 2.1
        $nav.on('click', function () {
            if (!isFixed) setTimeout(function () { 
                    $win.scrollTop($win.scrollTop() - 47) 
                }, 10)
        })
        
        $win.on('scroll', processScroll)
        
        function processScroll() {
            var i, scrollTop = $win.scrollTop()
            if (scrollTop >= navTop && !isFixed) {
                isFixed = 1
                $nav.addClass('subnav-fixed')
            }
            else if (scrollTop <= navTop && isFixed) {
                isFixed = 0
                $nav.removeClass('subnav-fixed')
            }
        }
    })
}(window.jQuery)

function runMiniClock() {
    var time = new Date();
    var hours = time.getHours();
    var minutes = time.getMinutes();
    var seconds = time.getSeconds();
    seconds=((seconds < 10) ? "0" : "") + seconds;
    minutes=((minutes < 10) ? "0" : "") + minutes;
    hours=(hours > 24) ? hours-24 : hours;
    hours=(hours == 0) ? 0 : hours;
    var clock = hours + ":" + minutes + ":" + seconds;
    if(clock != document.getElementById('clock').innerHTML) document.getElementById('clock').innerHTML = clock;
    timer = setTimeout("runMiniClock()",1000);
}

function setDatePickerOption() {
    $.datepicker.regional['ru'] = {
        closeText: 'Закрыть',
        prevText: '&#x3c;Пред',
        nextText: 'След&#x3e;',
        currentText: 'Сегодня',
        monthNames: ['Январь','Февраль','Март','Апрель','Май','Июнь',
        'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        monthNamesShort: ['Янв','Фев','Мар','Апр','Май','Июн',
        'Июл','Авг','Сен','Окт','Ноя','Дек'],
        dayNames: ['воскресенье','понедельник','вторник','среда','четверг','пятница','суббота'],
        dayNamesShort: ['вск','пнд','втр','срд','чтв','птн','сбт'],
        dayNamesMin: ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'],
        weekHeader: 'Не',
        dateFormat: 'dd.mm.yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['ru']);
    
    $.timepicker.regional['ru'] = {
        timeOnlyTitle: 'Выберите время',
        timeText: 'Время',
        hourText: 'Часы',
        minuteText: 'Минуты',
        secondText: 'Секунды',
        millisecText: 'миллисекунды',
        currentText: 'Сейчас',
        closeText: 'Закрыть',
        ampm: false
    };
    $.timepicker.setDefaults($.timepicker.regional['ru']);
    
    $('input[name=start], input[name=end]').datetimepicker({
        numberOfMonths: 2,
        hourGrid: 2,
        minuteGrid: 10,
        stepHour: 1,
        stepMinute: 5,
        timeFormat: 'hh:mm:ss'
    });
    
    $('input[name=birth_day], input[name=document_date]').datepicker({
        numberOfMonths: 1,
        showTime: false,
    });
}

function goSearchPerson(input_text) {
    //~ alert("goSearchPerson()"); //debug
    var div = input_text.next().children("fieldset");
    var query = input_text.val();
    if (query == '') { return false }
    div.load("/person/search/?query="+ query +"&destination="+ input_text.attr("name"));
    return false;
}




$(document).ready(function($) {
    runMiniClock();
    setDatePickerOption();
    
    var delay = (function(){
      var timer = 0;
      return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
      };
    })();
    
    $("#persons input.search").keyup(function() {
        goSearchPerson($(this));
    });
})


