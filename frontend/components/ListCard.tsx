import { Room } from "@/types/Room"

export default function ListCard({ room }: { room: Room }) {
  if (room.attributes.Description !== undefined) {
    return null
  }

  const rooms = JSON.parse(room.attributes.rooms)

  return (
    <div className="p-4 m-2 w-full border rounded shadow">
      <h2 className="text-lg font-semibold mb-2">{room.attributes.name}</h2>
      <p className="text-sm text-gray-600">Total Rooms: {room.attributes.total_rooms}</p>

      {rooms.map((r: any, index: number) => (
        <div key={index} className="mt-4 p-4 border rounded bg-gray-50">
          <h3 className="font-semibold text-md mb-2">Room {r.room_number}</h3>
          <div>
            {r.schedule.map((session: any, idx: number) => (
              <div key={idx} className="mb-2 p-2 bg-white rounded shadow-sm">
                <p className="text-sm font-medium">{session.course_name}</p>
                <p className="text-sm text-gray-700">
                  <strong>Instructor:</strong> {session.instructor || "TBA"}
                </p>
                <p className="text-sm text-gray-700">
                  <strong>Day:</strong> {session.day}
                </p>
                <p className="text-sm text-gray-700">
                  <strong>Time:</strong> {session.start_time} - {session.end_time}
                </p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
