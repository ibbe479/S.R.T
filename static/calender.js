$("#calender").on("change", function() {
    const valtDatum = $(this).val();

    $("main").addClass("is-blurred");

    $("#tid").show().css({
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "z-index": "9999",
        "filter": "none" // Se till att denna INTE är suddig
    });

    $("#v_datum").text("Datum: " + valtDatum)

    const start = $("#start_tid").val()
    const end = $("#slut_tid").val()

    $("#spara").on("click",function(){
      $("#tid").hide()
        $("main").removeClass("is-blurred");  
    })
    
    console.log("start : " + valtDatum + start )
    console.log("slut : " + valtDatum + end)
});