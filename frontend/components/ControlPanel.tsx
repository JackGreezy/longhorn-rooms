import { FaList, FaMapLocationDot } from "react-icons/fa6"
import { Room } from "@/types/Room"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"

interface ControlPanelProps {
  view: "map" | "list"
  setView: (view: "map" | "list") => void
  rooms: Room[]
  setRooms: React.Dispatch<React.SetStateAction<Room[]>>
}

export default function ControlPanel({ view, setView, rooms, setRooms }: ControlPanelProps) {
  return (
    <div className="w-72 p-4 border-r border-gray-300">
      <img src="/longhorn-rooms-primary.png" alt="Logo" className="h-10 mr-4 mb-4" />
      <div className="flex space-x-4 justify-center">
        <button
          onClick={() => setView("map")}
          className={`px-4 py-2 flex flex-col items-center justify-center rounded border bg-transparent  ${
            view === "map" ? "text-burntorange border-burntorange" : "text-gray-600"
          }`}
        >
          <FaMapLocationDot className="w-8 h-8" />
          <span className="font-semibold mt-2">Map View</span>
        </button>

        <button
          onClick={() => setView("list")}
          className={`px-4 py-2 flex flex-col items-center justify-center rounded border bg-transparent ${
            view === "list" ? "text-burntorange border-burntorange" : " text-gray-600"
          }`}
        >
          <FaList className="w-8 h-8" />
          <span className="font-semibold mt-2">List View</span>
        </button>
      </div>
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-4">Select Time</h3>

        <div className="flex flex-col mb-4">
          <Label htmlFor="start-time" className="mb-1">
            Start Time
          </Label>
          <Select>
            <SelectTrigger className="w-full">
              <SelectValue id="start-time" placeholder="Select start time" />
            </SelectTrigger>
            <SelectContent className="bg-white">
              <SelectItem value="08:00">08:00 AM</SelectItem>
              <SelectItem value="09:00">09:00 AM</SelectItem>
              <SelectItem value="10:00">10:00 AM</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex flex-col">
          <Label htmlFor="end-time" className="mb-1">
            End Time
          </Label>
          <Select>
            <SelectTrigger className="w-full">
              <SelectValue id="end-time" placeholder="Select end time" />
            </SelectTrigger>
            <SelectContent className="bg-white">
              <SelectItem value="16:00">04:00 PM</SelectItem>
              <SelectItem value="17:00">05:00 PM</SelectItem>
              <SelectItem value="18:00">06:00 PM</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  )
}
