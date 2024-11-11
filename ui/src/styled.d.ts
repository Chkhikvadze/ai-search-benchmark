// import original module declarations
import "styled-components";

// and extend them!
declare module "styled-components" {
  export interface DefaultTheme {
    body: {
      avatarDropDownColor: string;
      backgroundColorPrimary: string;
      backgroundColorSecondary: string;
      boxShadow: string;
      backdropFilter: string;
      textColorPrimary: string;
      textColorSecondary: string;
      backgroundImage: string;
      backgroundImageSecondary: string;
      testVariableColor: string;
      border: string;
      secondaryBorder: string;
      secondaryBorderBackground: string;
      iconColor: string;
      mainNavColor: string;
      mainNavColorActive: string;
      breadCrumbsColor: string;
      breadCrumbsBg: string;
      commandBorderColor: string;
      placeHolderColor: string;
      cardBgColor: string;
      humanMessageBgColor: string;
      replyBoxBgColor: string;
      secondaryIconColor: string;
      detailCardBackgroundColor: string;
      toolkitCardBgColorPrimary: string;
      toolkitCardBgColorSecondary: string;
      toolkitCardBgColorTertiary: string;
      teamChatCardSelectedColor: string;
      componentsWrapperBg: string;
      componentsSecondaryWrapperBg: string;
      textareaBorder: string;
      textAreaBgColor: string;
      tertiaryIconColor: string;
      dropdownBgColor: string;
      dataLoaderCardBorder: string;
      textColorTertiary: string;
      tableBackgroundColor: string;
      sliderBackgroundColor: string;
      dropdownSecondaryBgColor: string;
      commandMenuBackgroundColor: string;
      warningToastTextColor: string;
      sessionDropdownBorder: string;
      tagColor: string;
      imageBrightness: string;
      dialogBorder: string;
      linkTextColor: string;
      textDisabled: string;
    };
    contentLoader: {
      bgColor: string;
      fgColor: string;
      mainBgColor: string;
      borderColor: string;
    };
    typography: {
      contentPrimary: string;
      contentSecondary: string;
      contentTertiary: string;
      contentQuaternary: string;
    };
    heading: {
      contentPrimary: string;
      contentSecondary: string;
      contentTertiary: string;
    };
    button: {
      primary: ButtonStyleProps;
      secondary: ButtonStyleProps;
      tertiary: ButtonStyleProps;
    };
    textFiled: {
      primary: {
        color: string;
        bgColor: string;
        borderColor: string;
        activeBoxShadow: string;
        activeBorderColor: string;
        activeBgColor: string;
        errorBorderColor: string;
        errorColor: string;
      };
    };
    tabs: {
      color: string;
      hoverBgColor: string;
      activeColor: string;
      activeBgColor: string;
      borderColor: string;
    };

    // new colors
    basicForeground: {
      white: string;
      white8: string;
      white6: string;
      white4: string;
      white3: string;
      white2: string;
      white1: string;
      black1: string;
      black2: string;
      black3: string;
      black5: string;
      black7: string;
      black8: string;
      black: string;
    };
    foundation: {
      primaryA: string;
      primaryB: string;
      accentBlue: string;
      accentYellow: string;
      accentGreen: string;
      negative: string;
      warning: string;
      positive: string;
      purple: string;
      beige: string;
    };
    core: {
      background: {
        backgroundPrimary: string;
        backgroundSecondary: string;
        backgroundTertiary: string;
        backgroundElementsA: string;
        backgroundElementsB: string;
        backgroundMain: string;
      };
      content: {
        contentPrimary: string;
        contentSecondary: string;
        contentTertiary: string;
        contentQuaternary: string;
      };
      border: {
        borderPrimary: string;
        borderSecondary: string;
        borderTertiary: string;
        borderQuaternary: string;
        borderSelectedA: string;
        borderSelectedB: string;
        borderSelectedC: string;
      };
    };
    coreExtensions: {
      background: {
        backgroundDisabled: string;
        backgroundOverlayDark: string;
        backgroundOverlayLight: string;
        backgroundAccent: string;
        backgroundNegative: string;
        backgroundWarning: string;
        backgroundPositive: string;
      };
      content: {
        contentDisabled: string;
        contentExtra: string;
        contentExtra6: string;
        contentAccent: string;
        contentNegative: string;
        contentWarning: string;
        contentPositive: string;
      };
      border: {
        borderDisabled: string;
        borderHover: string;
        borderPressed: string;
        borderNegative: string;
        borderWarning: string;
        borderPositive: string;
      };
      multiplayer: {
        mpGray: string;
        mpGreen: string;
        mpPink: string;
        mpLightBlue: string;
        mpRed: string;
        mpBlue: string;
        mpPurple: string;
      };
      tags: {
        tagsBlack: string;
        tagsWhite: string;
        tagsGrey: string;
        tagsGreen: string;
        tagsPink: string;
        tagsLightBlue: string;
        tagsRed: string;
        tagsBlue: string;
        tagsPurple: string;
        tagsYellow: string;
        tagsOrange: string;
      };
    };
  }
}

type ButtonStyleProps = {
  color: string;
  bgColor: string;
  hoverBgColor: string;
  pressedBgColor: string;
  pressedBorderColor: string;
};
