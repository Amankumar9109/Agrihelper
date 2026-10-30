/**
 * SVG Vector Path Definitions for States & Union Territories of India
 * Canvas ViewBox: 0 0 650 720
 */
const INDIA_MAP_STATES = [
  {
    id: "JK",
    name: "Jammu and Kashmir",
    labelX: 200,
    labelY: 75,
    d: "M 165,30 L 225,25 L 260,60 L 275,100 L 255,130 L 210,125 L 180,120 L 160,85 Z"
  },
  {
    id: "HP",
    name: "Himachal Pradesh",
    labelX: 220,
    labelY: 135,
    d: "M 205,125 L 255,130 L 265,155 L 245,175 L 210,165 L 200,140 Z"
  },
  {
    id: "PB",
    name: "Punjab",
    labelX: 175,
    labelY: 155,
    d: "M 165,135 L 205,128 L 210,165 L 195,190 L 160,175 L 155,150 Z"
  },
  {
    id: "UT",
    name: "Uttrakhand",
    labelX: 265,
    labelY: 165,
    d: "M 245,150 L 275,150 L 295,185 L 260,200 L 245,175 Z"
  },
  {
    id: "HR",
    name: "Haryana",
    labelX: 195,
    labelY: 185,
    d: "M 190,165 L 225,168 L 230,205 L 215,220 L 185,210 L 180,185 Z"
  },
  {
    id: "DL",
    name: "NCT of Delhi",
    labelX: 215,
    labelY: 198,
    d: "M 212,192 L 224,193 L 223,205 L 211,203 Z"
  },
  {
    id: "RJ",
    name: "Rajasthan",
    labelX: 140,
    labelY: 235,
    d: "M 145,165 L 185,175 L 185,210 L 225,225 L 215,285 L 170,300 L 120,290 L 95,245 L 110,195 Z"
  },
  {
    id: "UP",
    name: "Uttar Pradesh",
    labelX: 275,
    labelY: 240,
    d: "M 225,175 L 260,195 L 325,220 L 375,255 L 350,290 L 290,295 L 260,270 L 225,260 L 215,225 Z"
  },
  {
    id: "GJ",
    name: "Gujarat",
    labelX: 95,
    labelY: 340,
    d: "M 85,285 L 140,295 L 155,340 L 135,385 L 105,380 L 115,355 L 85,350 L 60,335 L 65,305 Z"
  },
  {
    id: "MP",
    name: "Madhya Pradesh",
    labelX: 235,
    labelY: 330,
    d: "M 175,295 L 260,270 L 300,295 L 325,325 L 310,375 L 245,380 L 185,375 L 155,340 Z"
  },
  {
    id: "BR",
    name: "Bihar",
    labelX: 385,
    labelY: 270,
    d: "M 345,245 L 415,250 L 425,285 L 380,300 L 345,285 Z"
  },
  {
    id: "JH",
    name: "Jharkhand",
    labelX: 385,
    labelY: 325,
    d: "M 355,295 L 415,295 L 420,345 L 370,360 L 345,330 Z"
  },
  {
    id: "WB",
    name: "West Bengal",
    labelX: 435,
    labelY: 330,
    d: "M 420,255 L 435,245 L 440,285 L 460,340 L 440,390 L 415,370 L 420,320 Z"
  },
  {
    id: "CT",
    name: "Chattisgarh",
    labelX: 315,
    labelY: 395,
    d: "M 305,325 L 340,335 L 345,395 L 325,455 L 295,435 L 295,380 Z"
  },
  {
    id: "OR",
    name: "Odisha",
    labelX: 380,
    labelY: 405,
    d: "M 345,360 L 415,355 L 425,410 L 375,445 L 335,420 Z"
  },
  {
    id: "MH",
    name: "Maharashtra",
    labelX: 185,
    labelY: 420,
    d: "M 130,375 L 235,370 L 295,385 L 295,435 L 245,465 L 195,480 L 150,470 L 140,410 Z"
  },
  {
    id: "GA",
    name: "Goa",
    labelX: 152,
    labelY: 512,
    d: "M 148,505 L 158,506 L 157,518 L 147,515 Z"
  },
  {
    id: "TG",
    name: "Telangana",
    labelX: 260,
    labelY: 460,
    d: "M 235,425 L 285,420 L 295,465 L 265,495 L 235,465 Z"
  },
  {
    id: "AP",
    name: "Andhra Pradesh",
    labelX: 275,
    labelY: 515,
    d: "M 285,445 L 350,440 L 345,490 L 295,570 L 265,565 L 260,505 L 295,475 Z"
  },
  {
    id: "KA",
    name: "Karnataka",
    labelX: 190,
    labelY: 520,
    d: "M 160,470 L 230,465 L 245,520 L 225,585 L 180,575 L 160,515 Z"
  },
  {
    id: "KL",
    name: "Kerala",
    labelX: 195,
    labelY: 630,
    d: "M 185,575 L 210,580 L 215,645 L 205,670 L 185,620 Z"
  },
  {
    id: "TN",
    name: "Tamil Nadu",
    labelX: 250,
    labelY: 620,
    d: "M 225,565 L 275,565 L 270,630 L 240,675 L 215,670 L 215,585 Z"
  },
  {
    id: "SK",
    name: "Sikkim",
    labelX: 435,
    labelY: 215,
    d: "M 428,205 L 442,205 L 443,225 L 428,223 Z"
  },
  {
    id: "AS",
    name: "Assam",
    labelX: 510,
    labelY: 265,
    d: "M 465,245 L 535,235 L 555,260 L 530,280 L 480,285 L 460,265 Z"
  },
  {
    id: "AR",
    name: "Arunachal Pradesh",
    labelX: 560,
    labelY: 210,
    d: "M 505,195 L 585,200 L 595,240 L 545,235 L 515,225 Z"
  },
  {
    id: "ML",
    name: "Meghalaya",
    labelX: 485,
    labelY: 290,
    d: "M 468,280 L 515,278 L 512,298 L 465,295 Z"
  },
  {
    id: "NL",
    name: "Nagaland",
    labelX: 565,
    labelY: 265,
    d: "M 555,250 L 575,255 L 570,285 L 550,275 Z"
  },
  {
    id: "MN",
    name: "Manipur",
    labelX: 560,
    labelY: 305,
    d: "M 550,285 L 572,290 L 565,325 L 545,315 Z"
  },
  {
    id: "MZ",
    name: "Mizoram",
    labelX: 540,
    labelY: 345,
    d: "M 535,320 L 555,322 L 550,365 L 532,355 Z"
  },
  {
    id: "TR",
    name: "Tripura",
    labelX: 510,
    labelY: 330,
    d: "M 505,315 L 525,315 L 520,345 L 500,340 Z"
  },
  {
    id: "AN",
    name: "Andaman and Nicobar",
    labelX: 540,
    labelY: 580,
    d: "M 535,540 L 545,540 L 545,640 L 535,640 Z"
  }
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { INDIA_MAP_STATES };
}
