import { Room } from "@/types/Room"

export default function ListCard({ room }: { room: Room }) {
  if (!room.id || !room.attributes.Name) {
    return null
  }

  return (
    <div className="p-4 m-2 w-full border rounded shadow">
      <p className="font-semibold">Name: {room.attributes.Name}</p>
      <p>ID: {room.id}</p>
    </div>
  )
}
