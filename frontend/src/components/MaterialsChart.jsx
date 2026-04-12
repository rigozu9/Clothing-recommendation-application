import { useState } from "react";

const materialInfo = {
  canvas: {
    label: "Canvas",
    note: "You seem to like sturdy, practical fabrics with a casual edge.",
  },
  cashmere: {
    label: "Cashmere",
    note: "Your taste leans soft, elevated, and a little luxurious.",
  },
  chambray: {
    label: "Chambray",
    note: "You like light, relaxed fabrics with an effortless everyday feel.",
  },
  chiffon: {
    label: "Chiffon",
    note: "You gravitate toward airy, delicate, and more elegant textures.",
  },
  corduroy: {
    label: "Corduroy",
    note: "You seem to enjoy textured fabrics with a vintage personality.",
  },
  cotton: {
    label: "Cotton",
    note: "You often like soft, breathable, and easy-to-wear materials.",
  },
  denim: {
    label: "Denim",
    note: "Your picks suggest a casual, classic style with a bit of 70s attitude.",
  },
  faux_fur: {
    label: "Faux Fur",
    note: "You like bold texture and statement pieces that stand out.",
  },
  flannel: {
    label: "Flannel",
    note: "Your style leans cozy, relaxed, and comfort-first.",
  },
  fleece: {
    label: "Fleece",
    note: "You seem drawn to warm, soft materials made for comfort.",
  },
  gingham: {
    label: "Gingham",
    note: "You like playful fabrics with a neat and classic feel.",
  },
  knit: {
    label: "Knit",
    note: "You often prefer soft stretch and easy everyday comfort.",
  },
  lace: {
    label: "Lace",
    note: "You gravitate toward decorative details and a more delicate look.",
  },
  leather: {
    label: "Leather",
    note: "Your style has a structured, confident, and slightly edgy side.",
  },
  linen: {
    label: "Linen",
    note: "You seem to like breathable fabrics with a relaxed natural feel.",
  },
  neoprene: {
    label: "Neoprene",
    note: "You’re drawn to modern, sporty materials with a sleek structure.",
  },
  nylon: {
    label: "Nylon",
    note: "Your choices suggest lightweight, practical, and performance-friendly fabrics.",
  },
  organza: {
    label: "Organza",
    note: "You lean toward sheer, crisp fabrics with a dressed-up mood.",
  },
  patent: {
    label: "Patent",
    note: "You like polished finishes that add shine and drama.",
  },
  plush: {
    label: "Plush",
    note: "You seem to love soft textures that feel warm and expressive.",
  },
  polyester: {
    label: "Polyester",
    note: "You often pick versatile synthetic fabrics common in many everyday pieces.",
  },
  rayon: {
    label: "Rayon",
    note: "Your taste leans fluid, polished, and a little more refined.",
  },
  satin: {
    label: "Satin",
    note: "You’re drawn to smooth, glossy fabrics with a dressed-up feel.",
  },
  silk: {
    label: "Silk",
    note: "Your picks suggest elegant taste with a soft luxurious touch.",
  },
  spandex: {
    label: "Spandex",
    note: "You seem to like flexible, body-hugging materials with stretch.",
  },
  suede: {
    label: "Suede",
    note: "You gravitate toward rich texture and a softer take on structured style.",
  },
  taffeta: {
    label: "Taffeta",
    note: "You like crisp fabrics that feel formal, dramatic, and occasion-ready.",
  },
  tulle: {
    label: "Tulle",
    note: "Your style has a playful, light, and decorative side.",
  },
  tweed: {
    label: "Tweed",
    note: "You seem to enjoy classic tailoring and timeless textured fabrics.",
  },
  twill: {
    label: "Twill",
    note: "You like durable everyday fabrics with clean structure.",
  },
  velour: {
    label: "Velour",
    note: "You’re drawn to soft fabrics with a rich and cozy finish.",
  },
  velvet: {
    label: "Velvet",
    note: "Your style leans rich, expressive, and a little dramatic.",
  },
  vinyl: {
    label: "Vinyl",
    note: "You like bold, glossy materials that make more of a statement.",
  },
  wool: {
    label: "Wool",
    note: "You seem to prefer warm, classic fabrics with a timeless feel.",
  },
};

const formatMaterialName = (name) => {
  return name
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

const MaterialsChart = ({ data }) => {
  const [showAll, setShowAll] = useState(false);
  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  const visibleMaterials = (showAll ? data : data.slice(0, 5)).map((item) => {
    const normalizedName = item.name.toLowerCase();
    const info = materialInfo[normalizedName];

    return {
      ...item,
      percentage: totalValue > 0 ? (item.value / totalValue) * 100 : 0,
      label: info?.label || formatMaterialName(item.name),
      note: info?.note || "This material appears frequently in your liked items.",
    };
  });

  return (
    <div className="bg-gray-800 rounded-xl shadow border border-gray-700 p-6 w-full max-w-5xl">
      <h2 className="text-2xl font-semibold mb-2">Your Top Materials</h2>
      <p className="text-gray-400 mb-6">
        Materials you tend to prefer most, ranked from strongest to weakest.
      </p>

      {visibleMaterials.length < 10 ? (
        <div className="rounded-xl border border-gray-700 bg-gray-900/60 px-4 py-3">
          <p className="text-gray-400 text-base">Like more items to get material insights</p>
        </div>
      ) : (
        <div className="space-y-4">
          {visibleMaterials.map((item, index) => (
            <div
              key={item.name}
              className="bg-gray-900/60 border border-gray-700 rounded-2xl p-5"
            >
              <div className="flex items-start justify-between gap-4 mb-2">
                <div>
                  <p className="text-sm text-gray-400 mb-1">#{index + 1}</p>
                  <h3 className="text-xl font-semibold text-white">
                    {item.label}
                  </h3>
                </div>

                <div className="text-right flex-shrink-0">
                  <p className="text-2xl font-bold text-white">
                    {Math.round(item.percentage)}%
                  </p>
                  <p className="text-sm text-gray-400">
                    {item.value} liked items
                  </p>
                </div>
              </div>

              <p className="text-gray-300 leading-relaxed">{item.note}</p>
            </div>
          ))}
          <div className="mt-4">
            {!showAll && data.length > 5 && (
              <button
                onClick={() => setShowAll(true)}
                className="text-sm text-gray-300 hover:text-white underline"
              >
                Show all materials
              </button>
            )}

            {showAll && (
              <button
                onClick={() => setShowAll(false)}
                className="text-sm text-gray-300 hover:text-white underline"
              >
                Show less
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MaterialsChart;