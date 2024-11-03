import { useState } from "react"
import dynamic from "next/dynamic"
import ListView from "@/components/ListView"
import ControlPanel from "@/components/ControlPanel"

interface FeatureData {
  id: string
  attributes: Record<string, any>
}

const CampusMap = dynamic(() => import("../components/CampusMap"), { ssr: false })

export default function HomePage() {
  const [features, setFeatures] = useState<FeatureData[]>([])
  const [view, setView] = useState<"map" | "list">("map")

  return (
    <div className="flex h-screen">
      <ControlPanel view={view} setView={setView} />
      <div className="flex-1">{view === "map" ? <CampusMap setFeatures={setFeatures} /> : <ListView />}</div>
    </div>
  )
}
