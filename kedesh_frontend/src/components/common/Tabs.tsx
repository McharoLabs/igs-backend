import React, { ReactNode, useState } from "react";

interface TabItemProps {
  title: string;
  icon?: ReactNode;
  children: ReactNode;
  disabled?: boolean;
  className?: string;
}

interface TabsProps {
  children: React.ReactElement<TabItemProps>[];
  className?: {
    container?: string;
    headers?: string;
    button?: string;
    activeButton?: string;
    icon?: string;
    title?: string;
    content?: string;
  };
}

export const Tabs: React.FC<TabsProps> = ({ children, className = {} }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <div className={`tabs-container ${className.container || ""}`}>
      <div
        className={`tab-headers flex space-x-4 border-b overflow-x-auto ${
          className.headers || ""
        }`}
      >
        {children.map((tab, index) => (
          <button
            key={index}
            className={`tab-button px-4 py-2 whitespace-nowrap ${
              index === activeIndex
                ? `border-b-2 border-primary text-primary ${
                    className.activeButton || ""
                  }`
                : `text-gray-500 ${className.button || ""}`
            } ${tab.props.disabled ? "opacity-50 cursor-not-allowed" : ""}`}
            onClick={() => !tab.props.disabled && setActiveIndex(index)}
            disabled={tab.props.disabled}
          >
            <span className="flex items-center space-x-2">
              {tab.props.icon && (
                <span className={`tab-icon ${className.icon || ""}`}>
                  {tab.props.icon}
                </span>
              )}
              <span className={`tab-title ${className.title || ""}`}>
                {tab.props.title}
              </span>
            </span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className={`tab-content mt-4 ${className.content || ""}`}>
        {children.map((tab, index) =>
          index === activeIndex ? (
            <div
              key={index}
              className={`tab-pane ${tab.props.className || ""}`}
            >
              {tab.props.children}
            </div>
          ) : null
        )}
      </div>
    </div>
  );
};

export const TabItem: React.FC<TabItemProps> = ({ children }) => {
  return <>{children}</>;
};
