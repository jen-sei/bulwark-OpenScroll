"use client";

import React from "react";
import { Area, CartesianGrid, ComposedChart, Legend, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { month: "Jan", nav: 1500000, price: 1.06 },
  { month: "Feb", nav: 1300000, price: 1.04 },
  { month: "Mar", nav: 1400000, price: 1.04 },
  { month: "Apr", nav: 1600000, price: 1.03 },
  { month: "May", nav: 1700000, price: 1.06 },
  { month: "Jun", nav: 1800000, price: 1.05 },
  { month: "Jul", nav: 1900000, price: 1.06 },
  { month: "Aug", nav: 2000000, price: 1.09 },
  { month: "Sep", nav: 1850000, price: 1.04 },
  { month: "Oct", nav: 1950000, price: 1.09 },
  { month: "Nov", nav: 2100000, price: 1.12 },
  { month: "Dec", nav: 2200000, price: 1.1 },
];

const formatLargeNumber = (value: number) => `${(value / 1_000_000).toFixed(1)}M`;

export default function PerformanceChart() {
  return (
    <div className="border border-brand-cream rounded-xl p-2 md:p-4 border-opacity-20 bg-brand-background">
      <h2 className="text-2xl font-medium">Overall Performance</h2>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <defs>
            {/* Vertical Line Pattern */}
            <pattern id="verticalLines" patternUnits="userSpaceOnUse" width="5" height="10">
              <line x1="5" y1="0" x2="5" y2="10" stroke="orange" strokeWidth="2" />
            </pattern>

            <linearGradient id="fadeGradient" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="white" stopOpacity="1" /> {/* Fully visible at top */}
              <stop offset="30%" stopColor="white" stopOpacity="0.6" /> {/* Start fading */}
              <stop offset="50%" stopColor="white" stopOpacity="0.3" /> {/* More fading */}
              <stop offset="100%" stopColor="white" stopOpacity="0" /> {/* Fully transparent at bottom */}
            </linearGradient>

            <mask id="fadeMask">
              <rect x="0" y="0" width="100%" height="100%" fill="url(#fadeGradient)" />
            </mask>
          </defs>

          <XAxis dataKey="month" stroke="#aaa" />
          <YAxis yAxisId="left" stroke="#C9C7BA" domain={[1000000, 2500000]} tickFormatter={formatLargeNumber} />
          <YAxis yAxisId="right" orientation="right" stroke="#C9C7BA" domain={[0.99, 1.11]} />
          <Tooltip />
          {/* <Legend /> */}
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />

          {/* Area Chart for NAV USDC */}
          <Area
            type="monotone"
            dataKey="nav"
            stroke="#F66435"
            fill="url(#verticalLines)"
            mask="url(#fadeMask)"
            yAxisId="left"
            fillOpacity={1}
          />

          {/* Line Chart for Token Price */}
          <Line
            type="monotone"
            dataKey="price"
            stroke="#F66435"
            yAxisId="right"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 3 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
