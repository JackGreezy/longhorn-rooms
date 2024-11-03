import { Room } from "@/types/Room"
import ListCard from "./ListCard"
import { useState } from "react"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet"

export default function ListView({ rooms }: { rooms: Room[] }) {
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null)
  const [isSheetOpen, setIsSheetOpen] = useState(false)

  const handleCardClick = (room: Room) => {
    setSelectedRoom(room)
    setIsSheetOpen(true)
  }

  return (
    <div className="flex flex-wrap items-center justify-center h-full p-4">
      {rooms.map((room) => (
        <div key={room.id} onClick={() => handleCardClick(room)} className="w-full">
          <ListCard key={room.id} room={room} />
        </div>
      ))}

      <Sheet open={isSheetOpen} onOpenChange={setIsSheetOpen}>
        <SheetContent className="bg-white">
          <SheetHeader>
            <SheetTitle>{selectedRoom?.attributes.Name || "Room Details"}</SheetTitle>
            <SheetDescription>ID: {selectedRoom?.id}</SheetDescription>
          </SheetHeader>
        </SheetContent>
      </Sheet>
    </div>
  )
}
