import { useState } from "react"
import dynamic from "next/dynamic"
import ListView from "@/components/ListView"
import ControlPanel from "@/components/ControlPanel"
import Header from "@/components/Header"
import { Room } from "@/types/Room"

const CampusMap = dynamic(() => import("../components/CampusMap"), { ssr: false })

export default function HomePage() {
  const [rooms, setRooms] = useState<Room[]>([])
  const [view, setView] = useState<"map" | "list">("map")

  return (
    <div className="flex flex-col h-screen">
      {/* <Header /> */}
      <div className="flex flex-1">
        <ControlPanel view={view} setView={setView} rooms={rooms} setRooms={setRooms} />
        <div className="flex-1">{view === "map" ? <CampusMap setRooms={setRooms} /> : <ListView rooms={rooms} />}</div>
      </div>
    </div>
  )
}
