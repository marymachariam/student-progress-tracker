"use client";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend
);

export default function ProgressLineChart() {

    const data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
            {
                label: "Study Hours",
                data: [2, 3, 1.5, 4, 2.5, 5, 3],
                borderColor: "#0d6efd",
                backgroundColor: "rgba(13,110,253,.2)",
                tension: 0.4,
                fill: true
            }
        ]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: "top"
            }
        }
    };

    return (
        <div className="card shadow-sm mt-4">
            <div className="card-body">
                <h5>Weekly Study Progress</h5>

                <Line
                    data={data}
                    options={options}
                />
            </div>
        </div>
    );
}