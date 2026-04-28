$("#calender").on("change", function() {
    const valtDatum = $(this).val();

    $("main").addClass("is-blurred");
    $("#v_datum").text("Datum: " + valtDatum);

    $("#tid").show().css({
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "z-index": "9999"
    });

    $("#spara").off("click").on("click", function() {
        const start = $("#start_tid").val();
        const end = $("#slut_tid").val();
        
        let pass_lista = [];

        // Vi loopar igenom alla valda medlemmar
        $("#tid input[name='vem_i_teamet']:checked").each(function() {
            let email = $(this).val();
            
            // För varje person skapar vi ett eget objekt enligt ditt önskemål
            let person_pass = {
                "user_id": email,
                "start_shift": valtDatum + " " + start + ":00",
                "end_shift": valtDatum + " " + end + ":00"
            };
            
            pass_lista.push(person_pass);
        });

        if (start && end && start < end && pass_lista.length > 0) {
            $.ajax({
                url: '/skapa_pass',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(pass_lista), 
                success: function(response) {
                    $("#tid").hide();
                    $("main").removeClass("is-blurred");
                    $("#tid input[name='vem_i_teamet']").prop("checked", false);
                },
                error: function() {
                    alert("Kunde inte spara passen.");
                }
            });

        } else {
            alert("Kontrollera tiderna och välj minst en medlem.");
        }
    });
});