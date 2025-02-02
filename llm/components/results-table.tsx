import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface Entity {
  entity: string
  type: string
}

interface ResultsTableProps {
  title: string
  entities: Entity[]
}

export function ResultsTable({ title, entities }: ResultsTableProps) {
  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[200px]">Entity</TableHead>
            <TableHead>Type</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {entities.map((entity, i) => (
            <TableRow key={i}>
              <TableCell className="font-medium">{entity.entity}</TableCell>
              <TableCell>{entity.type}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

