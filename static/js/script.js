var users = [
    { 'fields': { 'first_name': 'Vasya1', 'last_name': 'Pupkin1' }},
    { 'fields': { 'first_name': 'Vasya2', 'last_name': 'Pupkin2' }},
    { 'fields': { 'first_name': 'Vasya2', 'last_name': 'Pupkin2' }},
    { 'fields': { 'first_name': 'Vasya3', 'last_name': 'Pupkin3' }},
    { 'fields': { 'first_name': 'Vasya4', 'last_name': 'Pupkin4' }},
    { 'fields': { 'first_name': 'Vasya5', 'last_name': 'Pupkin5' }},
    { 'fields': { 'first_name': 'Vasya6', 'last_name': 'Pupkin6' }},
    { 'fields': { 'first_name': 'Vasya7', 'last_name': 'Pupkin7' }},
];

$(function() {
    $('.btn-empty-trash').click(function() {
        $('.step').hide();
        $('.step.step-online-progress').show();

        $.getJSON('/get-online', function(data) {
            //users = data;

            var message = '';
            var gambling = false;
            if (users.length == 0) {
                message = 'Некому мусор выносить :(';
            } else if (users.length == 1) {
                message = 'Без альтернатив :)'
            } else {
                message = 'Людей в офисе: ' + users.length;
                gambling = true;
            }

            $('.step').hide();
            $('.step.step-online-list').show();
            $('.step.step-online-list .message').html(message);

            if (!gambling) {
                $('.step.step-online-list .btn-gambling').hide();
            }

            (function() {
                var online = $('.step.step-online-list .list-online');
                for (var i in users) {
                    var user = users[i].fields;
                    online.append('<div class="item">' + user.first_name + ' ' + user.last_name + '</div>');
                }
            })();
        }).error(function() {
            alert("error");
        })
    });

    $('.btn-gambling').click(function() {
        $('.step').hide();
        $('.step.step-gambling').show();

        var rand = Math.random();
        var delta = 360 / users.length;

        for (var i in users) {
            var user = users[i].fields;
            var item = $('<div class="item">' + user.first_name + ' ' + user.last_name + '</div>');
            item.css('-webkit-transform', 'rotateY(' + i * delta + 'deg) translateZ(700px)')
            $('.step.step-gambling .roulette').append(item);
        }
    });
})