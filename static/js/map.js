// 지도에 마커와 인포윈도우를 표시하는 함수입니다
function displayMarker(locPosition, message) {
            
    map.setCenter(locPosition);  // 지도 중심좌표를 접속위치로 변경합니다

    if(!message){
        searchDetailAddrFromCoords(locPosition, makeDetailAddr);

        // 마커를 클릭한 위치에 표시합니다 
        marker.setPosition(locPosition);
        marker.setMap(map);
    }
    else{
        marker.setPosition(locPosition);
        marker.setMap(map);

        //내용을 적은 인포윈도우를 마커 위에 표시합니다
        infowindow.setContent(message);
        infowindow.open(map, marker);
    }
}

function searchAddrFromCoords(coords, callback) {
    // 좌표로 행정동 주소 정보를 요청합니다
    geocoder.coord2RegionCode(coords.getLng(), coords.getLat(), callback);         
}

function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청합니다
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}

// 지도 좌측상단에 지도 중심좌표에 대한 주소정보를 표출하는 함수입니다
function displayCenterInfo(result, status) {
    if (status === kakao.maps.services.Status.OK) {
        var infoDiv = document.getElementById('centerAddr');

        for(var i = 0; i < result.length; i++) {
            // 행정동의 region_type 값은 'H' 이므로
            if (result[i].region_type === 'H') {
                infoDiv.innerHTML = result[i].address_name;
                break;
            }
        }
    }    
}

function makeDetailAddr(result, status) {
    if (status === kakao.maps.services.Status.OK) {
        var detailAddr = !!result[0].road_address ? '<div>도로명주소 : ' + result[0].road_address.address_name + '</div>' : '';
        detailAddr += '<div>지번 주소 : ' + result[0].address.address_name + '</div>';
        
        var content = '<div class="bAddr">' +
                        '<span class="title">법정동 주소정보</span>' + 
                        detailAddr + 
                    '</div>';

        // 인포윈도우에 클릭한 위치에 대한 법정동 상세 주소정보를 표시합니다
        infowindow.setContent(content);
        infowindow.open(map, marker);

        var loc = result[0].address.address_name;
        //여기서 주소 가져오기
        if(loc[4]=='구') tmp = loc.slice(3,5);
        else if(loc[5]=='구') tmp = loc.slice(3,6);
        else tmp = loc.slice(3,7);


        //여기는 지역이름 가져오는 api호출해주고, 지역이름 같이 넣어주기
        var eng_name = get_english_name(tmp);
        var data = get_airpollution(tmp);
        if(data){
        var table = document.getElementById('cur_loc');        
        table.innerHTML = "<td>" + tmp +"<br>" + eng_name + "</td>";
        table.innerHTML += "<td>" + data['GRADE'] + "</td>";
        table.innerHTML += "<td>" + data['POLLUTANT'] + "</td>";
        table.innerHTML += "<td>" + data['PM10'] + "</td>";
        table.innerHTML += "<td>" + data['PM25'] + "</td>";
        table.innerHTML += "<td>" + data['NITROGEN'] + "</td>";
        table.innerHTML += "<td>" + data['OZONE'] + "</td>";
        table.innerHTML += "<td>" + data['CARBON'] + "</td>";
        table.innerHTML += "<td>" + data['SULFUROUS'] + "</td>";
        table.innerHTML += "</table>";
        }
        else{
            alert("MyAir only shows status in Seoul!");
        }
    
    }   
}

function get_airpollution(loc){
    var result;

    $.ajax({
        url: "get_airpollution",
        data: {'loc': loc},
        datatype: "json",
        async: false,
        success: function(data){
            console.log("listAir ajax 성공");
            result = data['data'];
            console.log(result);
        },
        error:function(res){
            console.log("listAir ajax 실패");
        }
    });
    return result;
}

function get_avg_airpollution(){
    $.ajax({
        url: "get_avg_airpollution",
        data: null,
        datatype: "json",
        success: function(data){
            console.log("avgAir ajax 성공");
            var table = document.getElementById('avg_seoul');        
            table.innerHTML = "<td>" + data['data']['GRADE'] + "</td>";
            table.innerHTML += "<td>" + data['data']['POLLUTANT'] + "</td>";
            table.innerHTML += "<td>" + data['data']['PM10'] + "</td>";
            table.innerHTML += "<td>" + data['data']['PM25'] + "</td>";
            table.innerHTML += "<td>" + data['data']['NITROGEN'] + "</td>";
            table.innerHTML += "<td>" + data['data']['OZONE'] + "</td>";
            table.innerHTML += "<td>" + data['data']['CARBON'] + "</td>";
            table.innerHTML += "<td>" + data['data']['SULFUROUS'] + "</td>";
            table.innerHTML += "</table>"; 
        },
        error:function(res){
            console.log("avgAir ajax 실패");
        }
    });
}

function get_english_name(loc){
    var result;
    $.ajax({
        url: "get_english_name",
        data: {'loc':loc},
        datatype: "json",
        async : false,
        success: function(data){
            console.log("translate ajax 성공");
            result = data['data'];
        },
        error:function(res){
            console.log("translate ajax 실패");
        }
    });
    return result;
}