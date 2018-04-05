var authManager = (function() {
    var loginState = null;
    var intendedPath = null;

    var loggedIn = function (user) {
        loginState = {};
        loginState.loggedIn = true;
        loginState.user = user;
        page(intendedPath ? intendedPath : '/courier/list');
    };

    var initializeLogin = function(ctx, next) {
        if (loginState == null) {
            $.get({
                url: '/api/login',
                success: function (response) {
                    loggedIn(response.user);
                    next();
                },
                error: function (response) {
                    page('/logout');
                }
            });
        } else {
            console.log('Already logged in!');
            console.log(loginState);
            next();
        }
    };

    var showRegister = function () {
        viewManager.render('register', function ($view) {
            $view
                .find('form')
                .submitViaAjax(function (registerResponse) {
                    var form = this;
                    if (registerResponse.success) {
                        page('/')
                    } else {
                        $view.find('.message').text(registerResponse.message);
                    }
                });
        });
    };

    var getLoginState = function (cb) {
        if (loginState === null) {
            $.get({
                url: '/api/login',
                success: function (response) {
                    loginState = {};
                    if (response.success) {
                        loginState.loggedIn = true;
                        loginState.user = response.user;
                    } else {
                        loginState.loggedIn = false;
                    }
                    cb(loginState);
                },
                error: function (response) {
                    cb(loginState);
                }
            });
        } else {
            cb(loginState);
        }
    };

    var allowOnlyGuest = function (ctx, next) {
        getLoginState(function (state) {
            if (state.loggedIn) {
                page('/');
            } else {
                next();
            }
        });
    };

    var requiresMaster = function(ctx, next) {
        getLoginState(function (state) {
            console.log(state);
            if (state.user.master === true) { // Check if master
                next();
            } else {
                page('/'); // Go to main page
            }
        });
    };


    var aManager = {};
    aManager.initializeLogin = initializeLogin;
    aManager.showRegister = showRegister;
    aManager.allowOnlyGuest = allowOnlyGuest;
    aManager.requiresMaster = requiresMaster;
    return aManager;
})();
