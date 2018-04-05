var courierManager = (function () {
    var deleteCourier = function() {
        id = $(this).data('id');
        $.ajax({
            method: 'post',
            url: '/api/courier/' + id + '/delete',
            success: function(res) {
                listAll();
            }
        })
    }

    var listAll = function () {
        $.ajax({
            method: 'get',
            url: '/api/courier',
            success: function(res) {
                console.log(res.couriers);
                if (res.user.master === true) {
                    viewManager.render('couriers-list-master', {
                        couriers: res.couriers,
                    }, function($view) {
                        $view.find(".create-courier").click(function () { page('/courier/create'); });
                    });
                } else {
                    viewManager.render('couriers-list', {
                        couriers: res.couriers,
                    }, function($view) {
                       $view.find(".list-anonymous-couriers").click(function () { page('/courier/list-anonymous'); });
                    });
                }
            }
        });
    };

    var listAnonymous = function () {
        $.ajax({
            method: 'get',
            url: '/api/courier/anonymous',
            success: function(res) {
                console.log(res.couriers);
                viewManager.render('couriers-list-anonymous', {
                    couriers: res.couriers,
                }, function($view) {
                    $view.find(".list-all-couriers").click(listAll);
                });
            }
        });
    };

    var create = function () {
        $.ajax({
            method: 'get',
            url: '/api/user',
            success: function(res) {
                viewManager.render('courier', {
                    formAction: '/api/courier',
                    users: res.users
                }, function ($view) {
                    console.log($view);
                    $view.submitViaAjax(function (response) {
                        console.log(response);
                        if (response.success === true) {
                            console.log('Success!');
                                page('/courier/list');
                            }
                        else {
                            console.log('Failed');
                            $(":text").css('background-color', 'white');
                            $("textarea").css('background-color', 'white');
                            for (var field of response.fields) {
                                // console.log(field);
                                $('[name=' + field + ']').css('background-color', 'red');
                            }
                        }
                   });
                });
            }
        });
    };

    var listOne = function (id) {
        $.ajax({
            method: 'get',
            url: '/api/courier',
            success: function(res) {
                console.log(res.couriers[0]);
                viewManager.render('courier', res.couriers[0]);
            }
        })
    };

    var search = function(ctx) {
      var query = ctx.params.query;
      $.ajax({
            method: 'get',
            url: '/api/courier/search/' + query,
            success: function(res) {
                console.log(res.couriers);
                viewManager.render('couriers-list-master', {
                    couriers: res.couriers,
                }, function($view) {
                    $view.find(".create-courier").click(create);
                });
            }
        });  
    }
      var subReceived = function(ids){
        $.ajax({
        method:'POST',
        url:'/api/courier/subReceived',
        data:{ids: ids},
        success: function(res) {
                console.log("May the Force be with You")
            }
        });
        }

    var receivedList = function () {
        $.ajax({
            method: 'get',
            url: '/api/courier/received',
            success: function(res) {
                console.log(res.couriers);
                viewManager.render('couriers-list-master', {
                    couriers: res.couriers,
                }, function($view) {
                    $view.find(".list-all-couriers").click(listAll);
                });
            }
        });
    };
    var notReceivedList = function () {
        $.ajax({
            method: 'get',
            url: '/api/courier/notReceived',
            success: function(res) {
                console.log(res.couriers);
                viewManager.render('couriers-list-master', {
                    couriers: res.couriers,
                }, function($view) {
                    $view.find(".list-all-couriers").click(listAll);
                });
            }
        });
    };


    var showModify = function(id){
      $.ajax({
            method: 'get',
            url: '/api/courier/'+id,
            success: function(res){
                console.log(res);
                viewManager.render('modify', {
                    courier: res.courier,
                }, function($view) {
                    //$view.find(".list-all-couriers").click(listAll);
                    $view.find(".saveChange").click(function() {modify(id);});
                });
            }
        });
    };

    var modify=function(id){
      $.post("/api/courier/modify/" + id, $('form').serialize(),function(){page('/');});
    };



       var getRec=function (){
        var count=0;
        received=[];
        var a=document.getElementsByClassName("inp");
        for (i=0;i<a.length;i++)
             if (a[i].checked == true)
                 received[count++]=a[i].name;
        courierManager.subReceived(received);
        }





    var cManager = {};
    cManager.listAll = listAll;
    cManager.listOne = listOne;
    cManager.create = create;
    cManager.search = search;
    cManager.receivedList = receivedList;
    cManager.notReceivedList = notReceivedList;
    cManager.showModify=showModify;
    cManager.modify=modify;
    cManager.subReceived = subReceived;
    cManager.getRec=getRec;
    return cManager;
})();
