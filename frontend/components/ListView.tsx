import { Room } from "@/types/Room"
import ListCard from "./ListCard"

export default function ListView({ rooms, openAdditionalInfo }: { rooms: Room[]; openAdditionalInfo: (room: Room) => void }) {
  return (
    <div className="flex flex-wrap items-center justify-center h-full p-4">
      {rooms.map((room) => (
        <div key={room.id} className="w-full">
          <ListCard key={room.id} room={room} />
        </div>
      ))}
    </div>
  )
}
