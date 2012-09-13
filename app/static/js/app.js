/* app.js for Barbaris
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

/* App functions */

function setDateTimePickerObjects() {
    $('input[data-toggle=datetimepicker]').datetimepicker({
        dateFormat: 'yy-mm-dd',
        numberOfMonths: 2,
        hourGrid: 2,
        minuteGrid: 10,
        stepHour: 1,
        stepMinute: 5,
        timeFormat: 'hh:mm:ss'
    });
    
    $('input[data-toggle=datepicker]').datepicker({
        numberOfMonths: 1,
        showTime: false,
        dateFormat: 'yy-mm-dd',
    });
    
    $('input[data-toggle=timepicker]').timepicker({
        hourGrid: 2,
        minuteGrid: 10,
        stepHour: 1,
        stepMinute: 5,
    });
}

function setDateTimePickerOptions() {
    $.datepicker.regional['ru'] = {
        closeText: 'Закрыть',
        prevText: '&#x3c;Пред',
        nextText: 'След&#x3e;',
        currentText: 'Сейчас',
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
    
    setDateTimePickerObjects()
}

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
    if(clock != $('#clock').html()) $('#clock').html(clock);
    timer = setTimeout("runMiniClock()",1000);
}

function testLog(text) {
    console.log(text);
}

function goSearchClient(input_text) {
    //~ alert("goSearchClient()"); //debug
    var div = input_text.next().children("fieldset");
    var query = input_text.val();
    if (query == '') { return false }
    div.load("/client/search/?query="+ query +"&destination="+ input_text.attr("name"));
    return false;
}

function loadSPInfo() {
    //alert($(this).attr('data-toggle').replace(new RegExp("_",'g'), '/'));
    form = $(this);
    args = {};
    $(form).find('fieldset select').each(function() {
        args[$(this).attr('name')] = $(this).attr('value')
    });
    $(form).find('fieldset input:text').each(function() {
        args[$(this).attr('name')] = $(this).val()
    });
    testLog(args);
    div = form.siblings('div.sp-info');
    div.empty()
    div.load(
        '/specifications/info/', args, 
        function(data) { 
            div.removeClass('hidden');
        }
    );
}

function loadModal() {
    //alert($(this).attr('data-toggle').replace(new RegExp("_",'g'), '/'));
    a = $(this);
    w = $('#modalWindow');
    w.empty()
    w.load(
        a.attr('data-toggle').replace(new RegExp("_",'g'), '/'), 
        function(data) { 
            w.modal('toggle');
            setDateTimePickerObjects();
        }
    );
}

function updateMonitor() {
    $('a[rel=tooltip]').tooltip('hide');
    $('#monitor').load('/monitor/update/', function() {
        $("a[data-toggle^=_modal_]").click(loadModal);
        $('a[rel=tooltip]').tooltip();
    }
    );
}


/* Execute something after load page */
$(document).ready(function($) {
    runMiniClock();
    setDateTimePickerOptions();
    
    setInterval("updateMonitor()", 15000);
    
    $("#clients input.search").keyup(function() {
        goSearchClient($(this));
    });
    
    $("a[data-toggle^=_modal_]").click(loadModal);
    var path = window.location.pathname.split('/')[1]
    testLog(path)
    if (path) $('div.navbar a[href^="/' + path + '/"]').parents().addClass('active');
    else $('div.navbar a[href="/"]').parents().addClass('active');
    $('a[rel=tooltip]').tooltip();
    
    $('#categories form').change(loadSPInfo);
    
})
