"use client";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
);

export default function SubjectChart() {

    const data = {
        labels: [
            "Math",
            "Physics",
            "Programming",
            "English"
        ],

        datasets: [
            {
                label: "Hours",
                data: [10, 6, 15, 4],
                backgroundColor: [
                    "#0d6efd",
                    "#198754",
                    "#ffc107",
                    "#dc3545"
                ]
            }
        ]
    };

    return (
        <div className="card shadow-sm mt-4">
            <div className="card-body">

                <h5>Study Hours by Subject</h5>

                <Bar data={data} />

            </div>
        </div>
    );
}