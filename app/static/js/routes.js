// page('/', authManager.requiresAuthentication, courierManager.listAll);
// page('/courier/create', authManager.requiresAuthentication, authManager.requiresMaster, courierManager.create);
// page('/courier/search/:query', authManager.requiresAuthentication, authManager.requiresMaster, courierManager.search)
// page('/courier/:id', authManager.requiresAuthentication, courierManager.listOne);
page('/courier/list', authManager.initializeLogin, courierManager.listAll);
page('/courier/list-anonymous', authManager.initializeLogin, courierManager.listAnonymous);
//page('/courier/list-received', authManager.initializeLogin, courierManager.receivedList);
page('/courier/create', authManager.requiresMaster, courierManager.create);
page('/courier/search/:query', authManager.requiresMaster, courierManager.search)
page('/courier/:id', courierManager.listOne);

// page('/login', authManager.showLogin);
// page('/logout', authManager.logout);
page('/register', authManager.showRegister);

page({});
