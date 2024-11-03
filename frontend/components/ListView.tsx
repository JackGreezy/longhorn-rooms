import { Room } from "@/types/Room"
import ListCard from "./ListCard"

export default function ListView({ rooms }: { rooms: Room[] }) {
  return (
    <div className="flex flex-wrap items-center justify-center h-full p-4">
      {rooms.map((room) => (
        <ListCard key={room.id} room={room} />
      ))}
    </div>
  )
}
