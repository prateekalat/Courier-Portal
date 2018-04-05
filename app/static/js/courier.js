var makeCourier = function (courierData) {
    var data = {
        id: courierData.id,
        arrivalTime: courierData.arrivalTime,
        user: courierData.user,
        contents: courierData.contents
    };
    var getData = function () {
        return data;
    };
    var t = {};
    t.getData = getData;
    return t;
};
