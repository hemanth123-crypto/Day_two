const BASE_URL = "http://localhost:3000/bookings";

export async function getBookings() {

    try {

        const response = await fetch(BASE_URL);

        if (!response.ok) {
            throw new Error("Unable to fetch bookings");
        }

        return await response.json();

    } catch (error) {
        console.log(error.message);
    }

}