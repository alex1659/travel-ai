async function generateTrip() {

    const destination =
        document.getElementById(
            "destination"
        ).value;


    const days =
        Number(
            document.getElementById(
                "days"
            ).value
        );


    const budget =
        Number(
            document.getElementById(
                "budget"
            ).value
        );


    const selectedInterests =
        document.querySelectorAll(
            '.interests input:checked'
        );


    const interests = [];


    selectedInterests.forEach(
        checkbox => {

            interests.push(
                checkbox.value
            );

        }
    );


    if (!destination) {

        alert(
            "Please enter destination"
        );

        return;
    }


    if (!budget) {

        alert(
            "Please enter your budget"
        );

        return;
    }


    const result =
        document.getElementById(
            "result"
        );


    result.innerHTML =
        "<p>🤖 AI is planning your trip...</p>";


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/generate-itinerary",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        destination:
                            destination,

                        days:
                            days,

                        budget:
                            budget,

                        interests:
                            interests
                    })
                }
            );


        const data =
            await response.json();


        displayItinerary(data);


    } catch (error) {

        result.innerHTML =
            `
            <p>
                ❌ Could not connect to server.
            </p>
            `;

        console.error(error);
    }
}


function displayItinerary(data) {

    const result =
        document.getElementById(
            "result"
        );


    let html = `

        <h2>
            ✈️ Your ${data.days}-Day
            Trip to ${data.destination}
        </h2>

        <p>
            💰 Budget: ₹${data.budget}
        </p>

    `;


    data.itinerary.forEach(
        day => {

            html += `

                <div class="day">

                    <h3>
                        Day ${day.day}
                    </h3>

            `;


            day.activities.forEach(
                activity => {

                    html += `

                        <div class="activity">

                            <strong>
                                ${activity.time}
                            </strong>

                            <p>
                                ${activity.activity}
                            </p>

                        </div>

                    `;
                }
            );


            html += `

                </div>

            `;
        }
    );


    result.innerHTML = html;
}