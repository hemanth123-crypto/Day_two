const BASE_URL = "http://localhost:3000/bookings";

export async function deleteBooking(id) {

    try {

        await fetch(`${BASE_URL}/${id}`, {

            method: "DELETE"

        });

        console.log("Booking Deleted");

    } catch (error) {

        console.log(error.message);

    }

}