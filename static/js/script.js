var users = [];

$(function() {
    $('.btn-start').click(function() {
        $('.step').hide();
        $('.step.step-online-progress').show();

        $.getJSON('/get-online', function(data) {
            users = data.online;
            offlineUsers = data.offline;

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
                var offline = $('.step.step-online-list .list-offline');
                for (var i in users) {
                    var user = users[i];
                    online.append('<div class="item">' + user.first_name + ' ' + user.last_name + '</div>');
                }
                for (var i in offlineUsers) {
                    var user = offlineUsers[i];
                    offline.append('<div class="item">' + user.first_name + ' ' + user.last_name + '</div>');
                }
            })();
        }).error(function() {
            alert("error");
        })
    });

    $('.btn-gambling').click(function() {
        $('.step').hide();
        $('.step.step-gambling').show();

        if (!users || users.length == 0) {
            throw 'Users not found';
        }

        var userCount = users.length;
        var rand = Math.random();
        var looser = Math.floor(rand / (1 / userCount));

        for (var i = 0; i < looser; i++) {
            users.push(users.shift());
        }

        var delta = 360 / userCount;
        for (var i in users) {
            var user = users[i].fields;
            var item = $('<div class="item">' + user.first_name + ' ' + user.last_name + '</div>');
            item.css('-webkit-transform', 'rotateY(' + i * delta + 'deg) translateZ(700px)');
            $('.step.step-gambling .roulette').append(item);
        }
    });
})