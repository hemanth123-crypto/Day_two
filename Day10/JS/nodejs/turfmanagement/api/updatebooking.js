
// export async function updateBooking(id, booking) {

//     try {

//         const response = await fetch(`${BASE_URL}/${id}`, {

//             method: "PUT",

//             headers: {
//                 "Content-Type": "application/json"
//             },

//             body: JSON.stringify(booking)

//         });

//         return await response.json();

//     } catch (error) {

//         console.log(error.message);

//     }

// }

const BASE_URL = "http://localhost:3000/bookings";

export async function updateBooking(id, booking) {

    const response = await fetch(`${BASE_URL}/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(booking) //Convert an object to JSON

    });

    //return await response.json();
    if(!response.ok){
        console.log("Error booking ")
    }
    const booking = await response.json()
    console.log("Booking updated successfully")
    return booking
}