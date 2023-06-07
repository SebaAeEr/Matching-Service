function add_location(response) {
    document.getElementById("span_lname").innerHTML = response.name;
    document.getElementById("span_lid").innerHTML = response.id;
    document.getElementById("span_llong").innerHTML = response.long;
    document.getElementById("span_llat").innerHTML = response.lat;
    document.getElementById("span_lnum").innerHTML = response.tele_num;
    document.getElementById("span_lwebsite").innerHTML = response.website;
    document.getElementById("span_lreserve").innerHTML = response.reserve;
    document.getElementById("span_lmenu").innerHTML = response.menu;
    document.getElementById("span_laddress").innerHTML = response.address;
    document.getElementById("span_lorga_name").innerHTML = response.orga_id;
}

function add_orga(response) {
    document.getElementById("span_oname").innerHTML = response.orga_name;
    document.getElementById("span_oid").innerHTML = response.id;
    document.getElementById("span_oemail").innerHTML = response.email_address;
}

function add_event(response) {
    document.getElementById("span_ename").innerHTML = response.name;
    document.getElementById("span_eid").innerHTML = response.id;
    document.getElementById("span_estart_date").innerHTML = response.start_date;
    document.getElementById("span_eloc_id").innerHTML = response.loc_id;
    document.getElementById("span_eorga_id").innerHTML = response.orga_id;
    document.getElementById("span_eurl").innerHTML = response.url;
    document.getElementById("span_estart_time").innerHTML = response.url;
    document.getElementById("span_eprice").innerHTML = response.price;
    document.getElementById("span_edesc_all").innerHTML = response.desc_all;
}