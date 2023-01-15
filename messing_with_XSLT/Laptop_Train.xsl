<?xml version="1.0"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/sentences">
<sentences>
    <xsl:for-each select="sentence">
        <xsl:variable name="id" select="@id"/>
        <xsl:variable name="text" select="text"/>
        <xsl:choose>
            <xsl:when test="aspectTerms">
                <xsl:for-each select="aspectTerms/aspectTerm">
                    <sentence>
                        <id><xsl:value-of select="$id"/></id>
                        <text><xsl:value-of select="$text"/></text>
                        <aspectTerm><xsl:value-of select="@term"/></aspectTerm>
                        <from><xsl:value-of select="@from"/></from>
                        <to><xsl:value-of select="@to"/></to>
                        <polarity><xsl:value-of select="@polarity"/></polarity>
                    </sentence>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
                <sentence>
                    <id><xsl:value-of select="$id"/></id>
                    <text><xsl:value-of select="$text"/></text>
                </sentence>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>
</sentences>
</xsl:template>
</xsl:stylesheet>
