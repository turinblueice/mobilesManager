/**
 * Created by Administrator on 2017/2/14.
 */

/*
* summary:
*    借用手机
*
*@param  mobileId: 手机ID
* */
function borrowMobile(mobileId) {

    var borrowObj = {};
    borrowObj['mobile_id'] = mobileId;
    /*ajax发送请求数据*/
    $.post('/mobile/borrow/',  borrowObj, function (data,  status, jqxhr) {
        var retJsonObj = data;
        if(retJsonObj['succ'] == 0)
        {
            console.log("借用成功")
            alert("借用成功")
            window.location.reload()
        }
        else if(retJsonObj['succ'] == 1){
            alert(retJsonObj["message"])
            window.location = '/login/'
        }
        else
            alert(retJsonObj["message"])
    })

}


/*
* 归还手机
*
* @param mobileId  手机ID
*
* */
function giveBackMobile(mobileId) {
    var borrowObj = {};
    borrowObj['mobile_id'] = mobileId;
    /*ajax发送请求数据*/
    $.post('/mobile/give-back/',  borrowObj, function (data,  status, jqxhr) {
        var retJsonObj = data;
        if(retJsonObj['succ'] == 0)
        {
            console.log("归还成功")
            alert("归还成功")
            window.location.reload()
        }
        else{
            alert(retJsonObj["msg"])
        }
    })

}

$(function () {

    var mobileId = window.location.pathname.split('/')[2];

    $("#borrow").on('click', function (event) {
        borrowMobile(mobileId)
    })

    $("#give-back").on('click', function (event) {
        giveBackMobile(mobileId)
    })
})
