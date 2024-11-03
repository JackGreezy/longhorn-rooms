import { useState } from "react"
import dynamic from "next/dynamic"
import ListView from "@/components/ListView"
import ControlPanel from "@/components/ControlPanel"
import { Room } from "@/types/Room"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetTrigger } from "@/components/ui/sheet"

const CampusMap = dynamic(() => import("../components/CampusMap"), { ssr: false })

export default function HomePage() {
  const [rooms, setRooms] = useState<Room[]>([])
  const [view, setView] = useState<"map" | "list">("map")
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null)
  const [isSheetOpen, setIsSheetOpen] = useState(false)

  const openAdditionalInfo = (room: Room) => {
    setSelectedRoom(room)
    setIsSheetOpen(true)
  }

  return (
    <div className="flex flex-col h-screen">
      {/* <Header /> */}
      <div className="flex flex-1">
        <ControlPanel view={view} setView={setView} rooms={rooms} setRooms={setRooms} />
        <div className="flex-1">
          {view === "map" ? (
            <CampusMap setRooms={setRooms} openAdditionalInfo={openAdditionalInfo} />
          ) : (
            <ListView rooms={rooms} openAdditionalInfo={openAdditionalInfo} />
          )}
        </div>
      </div>
      <Sheet open={isSheetOpen} onOpenChange={setIsSheetOpen}>
        <SheetContent className="bg-white">
          <SheetHeader>
            <SheetTitle>{selectedRoom?.attributes.name || ""}</SheetTitle>
          </SheetHeader>
        </SheetContent>
      </Sheet>
    </div>
  )
}
