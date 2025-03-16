import Image from "next/image";

function FeatureCard({ title, description, imageSrc }: { title: string; description: string; imageSrc: string }) {
  return (
    <div className="bg-card bg-brand-dark rounded-lg p-4 md:p-8 pb-0 md:pb-0 flex flex-col flex-1 border border-brand-cream">
      <div className="mb-auto text-white font-inter font-light">
        <h2 className="text-2xl font-bold mb-3">{title}</h2>
        <p className="text-sm md:text-base opacity-90">{description}</p>
      </div>
      <div className="-mt-4 flex justify-center">
        <Image
          src={imageSrc || "/placeholder.svg"}
          alt={title}
          width={200}
          height={200}
          className="object-contain mix-blend-lighten"
        />
      </div>
    </div>
  );
}

export default FeatureCard;
