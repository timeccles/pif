-----------------------------------------------------------------------
-- pifcfg.vhd, 1200 version
--
-- Initial entry: 01-Ju1-13 te
-- non-common definitions to personalise the pif implementations
--
-----------------------------------------------------------------------
library ieee;                   use ieee.std_logic_1164.all;

package pifcfg is

  -- pif1200/7000 = 41h/42h = A/B
  constant PIF_ID      : std_logic_vector(7 downto 0) := x"41"; -- 'A'
  constant XO2_DENSITY : string                       := "1200L";

end package pifcfg;

-----------------------------------------------------------------------
package body pifcfg is
end package body pifcfg;

-----------------------------------------------------------------------
-- EOF pifcfg.vhd
