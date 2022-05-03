ticketEntries = [];
var enterButton = document.querySelector("#enter-button");

enterButton.onclick = function() 
{
	var newTicketInputEname = document.querySelector("#name-box");
	var newTicketInputEage = document.querySelector("#age-box");
	var newTicketInputGuest = document.querySelector("#guest-box");
	
	createTicketOnServer(newTicketInputEname.value, newTicketInputEage.value,
						 newTicketInputGuest.value);	
    newTicketInputEname = "";
	newTicketInputEage = "";
	newTicketInputGuest = "";
};

function createTicketOnServer( ename, eage, gname )
{
	var data = "entrant_name=" + encodeURIComponent(ename);
	data += "&entrant_age=" + encodeURIComponent(eage);
	data += "&guest_name=" + encodeURIComponent(gname);

	fetch("http://localhost:8080/tickets",
	{ 
		method: "POST",
		credentials: "include",
		body: data,
		headers: 
		{
			"Content-Type": "application/x-www-form-urlencoded"
		}
		
	}).then(function(response)
	{
		if (response.status == 403)
		{
			response.text().then(function(text)
			{
				console.log(text);
			});
		}
		loadTicketsFromServer();
	});
}

function loadTicketsFromServer()
{
    fetch("http://localhost:8080/tickets",
    {
        credentials: "include"
    }).then(function (response)
    {

        response.json().then(function (dataFromServer)
        {
            ticketEntries = dataFromServer;
            var ticketList = document.querySelector("#ticket-list");
            ticketList.innerHTML = "";
            ticketEntries.forEach((ticket) =>
            {
                var ticketEntryItem = document.createElement("li");

				var nameDiv = document.createElement("div");
				nameDiv.innerHTML = ticket.entrant_name;
				nameDiv.classList.add("entrant-name");
				ticketEntryItem.appendChild(nameDiv);

				var ageDiv = document.createElement("div");
				ageDiv.innerHTML = ticket.entrant_age;
				ageDiv.classList.add("entrant-age");
				ticketEntryItem.appendChild(ageDiv);
                
				var guestDiv = document.createElement("div");
				guestDiv.innerHTML = ticket.guest_name;
				guestDiv.classList.add("guest-name");
				ticketEntryItem.appendChild(guestDiv);

				var dayOfWeek = new Date().getDate();

				//code to display the random ticket number and the day of the week.
				///////////////////////////////////////////
				//var tokenDiv = document.createElement("div");
				//tokenDiv.innerHTML = ticket.random_token;
				//tokenDiv.classList.add("token-name");
				//ticketEntryItem.appendChild(tokenDiv);

				//var dayDiv = document.createElement("div");
				//dayDiv.innerHTML = dayOfWeek;
				//dayDiv.classList.add("day");
				//ticketEntryItem.appendChild(dayDiv);
				///////////////////////////////////////////
				if(dayOfWeek == ticket.random_token)
				{
					ticketEntryItem.style.backgroundColor = "goldenrod";
					ticketEntryItem.style.color = "purple";
					ticketEntryItem.style.borderColor = "purple";
				}
                ticketList.appendChild(ticketEntryItem);
            });
        });
    });
}

loadTicketsFromServer();